from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

import csv
import datetime
import itertools
import os
import re
import sys

import pyperclip

currentDirectory = os.path.dirname(os.path.realpath(__file__))
parentDirectory = os.path.dirname(currentDirectory)
sys.path.append(parentDirectory)

import chromagnonSession
import chromagnonGUI.chromagnonAbout
from chromagnon.sessionParse import decode_transition

# ---------------------------------------------------------------------------
# Command category sets used for row colour-coding
# ---------------------------------------------------------------------------
CLOSED_COMMANDS = frozenset({'CommandTabClosed', 'CommandWindowClosed'})
WINDOW_COMMANDS = frozenset({
    'CommandSetWindowBounds3', 'CommandSetWindowType', 'CommandSetWindowAppName',
    'CommandSetWindowUserTitle', 'CommandSetActiveWindow', 'CommandSetWindowWorkspace2',
    'CommandSetWindowVisibleOnAllWorkspaces', 'CommandAddWindowExtraData',
    'CommandSetSelectedTabInIndex',
})
GROUP_COMMANDS = frozenset({'CommandSetTabGroup', 'CommandSetTabGroupMetadata2'})
PRUNE_COMMANDS = frozenset({
    'CommandTabNavigationPathPrunedFromBack',
    'CommandTabNavigationPathPrunedFromFront',
    'CommandTabNavigationPathPruned',
})


class main_window(TkinterDnD.Tk):
    def __init__(self):
        TkinterDnD.Tk.__init__(self)
        self.geometry('1400x700')
        self.title('Chromagnon Session Viewer')
        self._all_commands = []
        self._iid_counter = 0
        self._group_by_tab = BooleanVar(value=False)
        self._build_menu()
        self._build_toolbar()
        self._build_treeview()
        self._build_status_bar()

    # -------------------------------------------------------------------
    # UI construction
    # -------------------------------------------------------------------

    def _build_menu(self):
        menubar = Menu(self)

        fileMenu = Menu(menubar, tearoff=0)
        fileMenu.add_command(label='Open\u2026', accelerator='Ctrl+O',
                             command=self.openFileDialog)
        fileMenu.add_separator()
        fileMenu.add_command(label='Export CSV\u2026', command=self.exportCSV)
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=self.quit)
        menubar.add_cascade(label='File', menu=fileMenu)
        self.bind('<Control-o>', lambda _: self.openFileDialog())

        viewMenu = Menu(menubar, tearoff=0)
        viewMenu.add_checkbutton(label='Group by Tab',
                                 variable=self._group_by_tab,
                                 command=self._refresh_view)
        menubar.add_cascade(label='View', menu=viewMenu)

        helpMenu = Menu(menubar, tearoff=0)
        helpMenu.add_command(label='About\u2026', command=self.showAbout)
        menubar.add_cascade(label='Help', menu=helpMenu)

        self.config(menu=menubar)

    def _build_toolbar(self):
        bar = Frame(self)
        bar.pack(fill=X, padx=8, pady=(6, 0))
        Label(bar, text='Filter:').pack(side=LEFT)
        self._search_var = StringVar()
        self._search_var.trace_add('write', lambda *_: self._refresh_view())
        Entry(bar, textvariable=self._search_var, width=50).pack(
            side=LEFT, padx=(4, 12))
        Label(bar,
              text='Drag and drop a Session or Tabs file here, or use File \u2192 Open',
              fg='grey').pack(side=LEFT)

    def _build_treeview(self):
        treeFrame = Frame(self)
        treeFrame.pack(fill=BOTH, expand=True, padx=8, pady=6)

        vscroll = Scrollbar(treeFrame)
        hscroll = Scrollbar(treeFrame, orient='horizontal')
        self.dataTable = ttk.Treeview(
            treeFrame,
            columns=('Timestamp', 'Type', 'ID', 'URL', 'Title'),
            yscrollcommand=vscroll.set,
            xscrollcommand=hscroll.set,
        )
        vscroll.config(command=self.dataTable.yview)
        hscroll.config(command=self.dataTable.xview)
        vscroll.pack(side=RIGHT, fill=Y)
        hscroll.pack(side=BOTTOM, fill=X)
        self.dataTable.pack(fill=BOTH, expand=True)

        self.dataTable.column('#0',          width=24,  minwidth=20,  stretch=False)
        self.dataTable.column('Timestamp',   width=175, minwidth=120)
        self.dataTable.column('Type',        width=215, minwidth=120)
        self.dataTable.column('ID',          width=100, minwidth=60)
        self.dataTable.column('URL',         width=540, minwidth=80)
        self.dataTable.column('Title',       width=280, minwidth=60)

        self.dataTable.heading('#0',        text='')
        self.dataTable.heading('Timestamp', text='Timestamp',   anchor=W)
        self.dataTable.heading('Type',      text='Type',         anchor=W)
        self.dataTable.heading('ID',        text='Tab/Win ID',   anchor=W)
        self.dataTable.heading('URL',       text='URL / Info',   anchor=W)
        self.dataTable.heading('Title',     text='Title',        anchor=W)

        style = ttk.Style()
        style.configure('Treeview', background='white')
        style.map('Treeview', background=[('selected', '#3399ff')])

        ## Row colour tags
        self.dataTable.tag_configure('nav',    background='#ffffff')
        self.dataTable.tag_configure('closed', background='#ffe5e5')
        self.dataTable.tag_configure('window', background='#e5f0ff')
        self.dataTable.tag_configure('group',  background='#fffde5')
        self.dataTable.tag_configure('prune',  background='#f0f0f0')
        self.dataTable.tag_configure('detail', background='#fafafa',
                                     foreground='#555555')
        self.dataTable.tag_configure('header', background='#d8d8d8',
                                     font=('TkDefaultFont', 9, 'bold'))

        ## Keyboard / mouse bindings
        self.dataTable.bind('<Control-c>', self.copyFromTreeview)
        self.dataTable.bind('<Button-2>',  self.handlePopUpMenu)
        self.dataTable.bind('<Button-3>',  self.handlePopUpMenu)

        self.popupMenu = Menu(self.dataTable, tearoff=0)
        self.popupMenu.add_command(label='Copy', command=self.copyFromTreeview)

        ## Drag-and-drop
        self.dataTable.drop_target_register(DND_FILES)
        self.dataTable.dnd_bind('<<Drop>>', self.processFileUpload)

    def _build_status_bar(self):
        self._status_var = StringVar(value='No file loaded')
        Label(self, textvariable=self._status_var, anchor=W,
              relief=SUNKEN, padx=4).pack(fill=X, side=BOTTOM)

    # -------------------------------------------------------------------
    # File loading
    # -------------------------------------------------------------------

    def openFileDialog(self):
        path = filedialog.askopenfilename(
            title='Open Session or Tabs file',
            filetypes=[
                ('Session / Tabs files', 'Session* Tabs* Current*'),
                ('All files', '*'),
            ],
        )
        if path:
            self.after_idle(self._loadSessionFile, path)

    def processFileUpload(self, event):
        ## Capture path immediately and defer heavy work so that tkinterdnd2
        ## can complete its XdndFinished handshake before we start parsing.
        filePath = event.data
        if filePath[0] == '{' and filePath[-1] == '}':
            filePath = filePath[1:-1]
        self.after_idle(self._loadSessionFile, filePath)

    def _loadSessionFile(self, filePath):
        try:
            self._all_commands = chromagnonSession.guiParse(filePath)
        except Exception as e:
            messagebox.showerror('Parse Error', str(e))
            return

        ## Update window title with decoded filename timestamp
        filename = os.path.basename(filePath)
        win_title = 'Chromagnon Session Viewer \u2014 ' + filename
        m = re.search(r'\d+$', os.path.splitext(filename)[0])
        if m:
            try:
                ts_val = int(m.group())
                file_dt = (datetime.datetime(1601, 1, 1) +
                           datetime.timedelta(microseconds=ts_val))
                win_title += ' (%s UTC)' % file_dt.strftime('%Y-%m-%d %H:%M:%S')
            except (OverflowError, ValueError):
                pass
        self.title(win_title)

        self._search_var.set('')
        self._refresh_view()

        nav_count = sum(1 for c in self._all_commands
                        if type(c).__name__ == 'CommandUpdateTabNavigation')
        self._status_var.set(
            '%s  |  %d commands  |  %d navigation entries'
            % (filename, len(self._all_commands), nav_count)
        )

    # -------------------------------------------------------------------
    # View rendering
    # -------------------------------------------------------------------

    def removeRecords(self):
        for iid in self.dataTable.get_children():
            self.dataTable.delete(iid)

    def _refresh_view(self):
        if not self._all_commands:
            return
        self.removeRecords()
        self._iid_counter = 0
        query = self._search_var.get().strip().lower()
        if self._group_by_tab.get():
            self._render_grouped(query)
        else:
            self._render_sequential(query)

    def _next_iid(self):
        iid = 'r%d' % self._iid_counter
        self._iid_counter += 1
        return iid

    def _matches(self, cmd, query):
        if not query:
            return True
        ts, type_str, id_str, url, title = self._get_display_fields(cmd)
        return query in (ts + type_str + id_str + (url or '') + (title or '')).lower()

    def _render_sequential(self, query):
        for cmd in self._all_commands:
            if self._matches(cmd, query):
                self._insert_command(cmd, parent='')

    def _render_grouped(self, query):
        tabs = {}
        other = []
        for cmd in self._all_commands:
            if type(cmd).__name__ == 'CommandUpdateTabNavigation':
                tabs.setdefault(cmd.tabId, []).append(cmd)
            else:
                other.append(cmd)

        ## Navigation entries grouped under a Tab header, sorted by nav index
        for tab_id in sorted(tabs):
            entries = sorted(tabs[tab_id], key=lambda c: c.index)
            visible = [c for c in entries if self._matches(c, query)]
            if not visible:
                continue
            tab_iid = '_tab_%d' % tab_id
            self.dataTable.insert(
                '', 'end', iid=tab_iid, text='',
                values=('', 'Tab %d  (%d entries)' % (tab_id, len(visible)),
                        'T:%d' % tab_id, '', ''),
                open=True, tags=('header',),
            )
            for cmd in visible:
                self._insert_command(cmd, parent=tab_iid)

        ## All other session commands under a Session Events header
        visible_other = [c for c in other if self._matches(c, query)]
        if visible_other:
            self.dataTable.insert(
                '', 'end', iid='_events', text='',
                values=('', 'Session Events  (%d entries)' % len(visible_other),
                        '', '', ''),
                open=True, tags=('header',),
            )
            for cmd in visible_other:
                self._insert_command(cmd, parent='_events')

    def _insert_command(self, cmd, parent):
        ts, type_str, id_str, url, title = self._get_display_fields(cmd)
        iid = self._next_iid()
        self.dataTable.insert(
            parent, 'end', iid=iid, text='',
            values=(ts, type_str, id_str, url or '', title or ''),
            tags=(self._get_tag(cmd),),
            open=False,
        )
        ## Child detail rows (navigation entries only)
        for label, value in self._get_detail_rows(cmd):
            child_iid = self._next_iid()
            self.dataTable.insert(
                iid, 'end', iid=child_iid, text='',
                values=('', label, '', value, ''),
                tags=('detail',),
            )

    # -------------------------------------------------------------------
    # Data-extraction helpers
    # -------------------------------------------------------------------

    def _get_display_fields(self, cmd):
        name = type(cmd).__name__.replace('Command', '', 1)

        ## Timestamp
        ts = ''
        if hasattr(cmd, 'timestamp') and cmd.timestamp:
            try:
                ts = str(datetime.datetime(1601, 1, 1) +
                         datetime.timedelta(microseconds=cmd.timestamp))
            except (OverflowError, ValueError):
                ts = str(cmd.timestamp)
        elif hasattr(cmd, 'closeTime'):
            ts = str(cmd.closeTime)
        elif hasattr(cmd, 'lastActiveTime'):
            ts = str(cmd.lastActiveTime) + ' *'

        ## Tab / Window ID
        id_str = ''
        if hasattr(cmd, 'tabId') and hasattr(cmd, 'windowId'):
            id_str = 'W:%d T:%d' % (cmd.windowId, cmd.tabId)
        elif hasattr(cmd, 'tabId'):
            id_str = 'T:%d' % cmd.tabId
        elif hasattr(cmd, 'windowId'):
            id_str = 'W:%d' % cmd.windowId
        elif hasattr(cmd, 'sessionId'):
            id_str = 'S:%d' % cmd.sessionId

        ## URL and Title (set on UpdateTabNavigation; others use _get_extra_info)
        url   = getattr(cmd, 'url',   '') or ''
        title = getattr(cmd, 'title', '') or ''
        if not url and not title:
            url = self._get_extra_info(cmd)

        return (ts, name, id_str, url, title)

    def _get_extra_info(self, cmd):
        """Return a short summary string for the URL/Info column for non-nav commands."""
        name = type(cmd).__name__
        if name in ('CommandTabClosed', 'CommandWindowClosed'):
            return 'Closed'
        if name == 'CommandLastActiveTime':
            return 'Last active (TimeTicks \u2014 approx.)'
        if name == 'CommandSetTabWindow':
            return 'Assign tab to window'
        if name == 'CommandSetTabIndexInWindow':
            return 'Index: %d' % getattr(cmd, 'index', '?')
        if name == 'CommandSetSelectedNavigationIndex':
            return 'Nav index: %d' % getattr(cmd, 'index', '?')
        if name == 'CommandSetSelectedTabInIndex':
            return 'Tab index: %d' % getattr(cmd, 'index', '?')
        if name == 'CommandSetWindowType':
            return 'Window type: %d' % getattr(cmd, 'windowType', '?')
        if name in PRUNE_COMMANDS:
            parts = []
            idx = getattr(cmd, 'index', None)
            cnt = getattr(cmd, 'count', None)
            if idx is not None:
                parts.append('index=%d' % idx)
            if cnt is not None:
                parts.append('count=%d' % cnt)
            return ', '.join(parts) if parts else 'Prune'
        if name == 'CommandSetPinnedState':
            return 'Pinned: %s' % bool(getattr(cmd, 'pinned', False))
        if name == 'CommandSetExtensionAppID':
            return 'App: %s' % getattr(cmd, 'extensionAppId', '')
        if name == 'CommandSetWindowBounds3':
            return 'x:%d y:%d  %d\u00d7%d  state:%s' % (
                cmd.x, cmd.y, cmd.w, cmd.h, cmd.state)
        if name == 'CommandSetWindowWorkspace2':
            return 'Workspace: %s' % getattr(cmd, 'workspaceGuid', '')
        if name == 'CommandSetWindowAppName':
            return 'App: %s' % getattr(cmd, 'appName', '')
        if name == 'CommandSetActiveWindow':
            return 'Active window'
        if name == 'CommandSessionStorageAssociated':
            return 'Storage: %s' % getattr(cmd, 'storageNamespace', '')
        if name == 'CommandSetTabGroup':
            hi = getattr(cmd, 'groupIdHigh', 0)
            lo = getattr(cmd, 'groupIdLow', 0)
            if hi == 0 and lo == 0:
                return 'Remove from group'
            return 'Group: %016x%016x' % (hi, lo)
        if name == 'CommandSetTabGroupMetadata2':
            return 'Group title: %s' % getattr(cmd, 'title', '')
        if name == 'CommandSetTabGuid':
            return 'GUID: %s' % getattr(cmd, 'guid', '')
        if name == 'CommandAddTabExtraData':
            return '%s = %s' % (getattr(cmd, 'key', ''), getattr(cmd, 'extraData', ''))
        if name == 'CommandAddWindowExtraData':
            return '%s = %s' % (getattr(cmd, 'key', ''), getattr(cmd, 'extraData', ''))
        if name == 'CommandSetTabUserAgentOverride2':
            ua = getattr(cmd, 'userAgentOverride', '')
            return 'UA: %s' % (ua or '(reset)')
        if name == 'CommandSetTabData':
            return str(getattr(cmd, 'data', ''))
        if name == 'CommandSetWindowUserTitle':
            return 'User title: %s' % getattr(cmd, 'userTitle', '')
        if name == 'CommandSetWindowVisibleOnAllWorkspaces':
            return 'All workspaces: %s' % getattr(cmd, 'visibleOnAllWorkspaces', '')
        return ''

    def _get_detail_rows(self, cmd):
        """Return (label, value) child rows — only populated for UpdateTabNavigation."""
        if type(cmd).__name__ != 'CommandUpdateTabNavigation':
            return []
        rows = []
        if hasattr(cmd, 'transition'):
            rows.append(('Transition', decode_transition(cmd.transition)))
        if getattr(cmd, 'http_status_code', None) is not None:
            rows.append(('HTTP Status', str(cmd.http_status_code)))
        if hasattr(cmd, 'has_post_data'):
            rows.append(('Has POST Data', str(cmd.has_post_data)))
        if getattr(cmd, 'referrer_url', ''):
            rows.append(('Referrer URL', cmd.referrer_url))
        if getattr(cmd, 'referrer_policy', None) is not None:
            rows.append(('Referrer Policy', str(cmd.referrer_policy)))
        if getattr(cmd, 'original_request_url', ''):
            rows.append(('Original URL', cmd.original_request_url))
        if getattr(cmd, 'is_overriding_user_agent', False):
            rows.append(('UA Override', 'Yes'))
        return rows

    def _get_tag(self, cmd):
        name = type(cmd).__name__
        if name in CLOSED_COMMANDS:
            return 'closed'
        if name in WINDOW_COMMANDS:
            return 'window'
        if name in GROUP_COMMANDS:
            return 'group'
        if name in PRUNE_COMMANDS:
            return 'prune'
        return 'nav'

    # -------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------

    def showAbout(self):
        chromagnonGUI.chromagnonAbout.main_window()

    def copyFromTreeview(self, event=None):
        rows = []
        for iid in self.dataTable.selection():
            vals = self.dataTable.item(iid)['values']
            rows.append('\t'.join(str(v) for v in vals))
        pyperclip.copy('\n'.join(rows))

    def handlePopUpMenu(self, event):
        row = self.dataTable.identify_row(event.y)
        if row:
            self.dataTable.selection_set(row)
        self.popupMenu.post(event.x_root, event.y_root)

    def exportCSV(self):
        if not self._all_commands:
            messagebox.showinfo('Export', 'No data to export.')
            return
        path = filedialog.asksaveasfilename(
            title='Export CSV',
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv'), ('All files', '*')],
        )
        if not path:
            return
        try:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Timestamp', 'Type', 'ID', 'URL', 'Title',
                    'Transition', 'HTTP Status', 'Has POST Data',
                    'Referrer URL', 'Referrer Policy', 'Original URL', 'UA Override',
                ])
                for cmd in self._all_commands:
                    ts, type_str, id_str, url, title = self._get_display_fields(cmd)
                    details = dict(self._get_detail_rows(cmd))
                    writer.writerow([
                        ts, type_str, id_str, url, title,
                        details.get('Transition', ''),
                        details.get('HTTP Status', ''),
                        details.get('Has POST Data', ''),
                        details.get('Referrer URL', ''),
                        details.get('Referrer Policy', ''),
                        details.get('Original URL', ''),
                        details.get('UA Override', ''),
                    ])
            messagebox.showinfo(
                'Export',
                'Exported %d rows to:\n%s' % (len(self._all_commands), path),
            )
        except Exception as e:
            messagebox.showerror('Export Error', str(e))


def main():
    root = main_window()
    root.mainloop()


if __name__ == '__main__':
    main()
