#include <std/string.pat>


// Some commands are obsolete and excluded for that reason.
enum command_type : u8 {
    SetTabWindow = 0,
    SetTabIndexInWindow = 2,
    TabClosed = 3,
    WindowClosed = 4,
    UpdateTabNavigationPathPrunedFromBack = 5,
    UpdateTabNavigation = 6,
    SetSelectedNavigationIndex = 7,
    SetSelectedTabInIndex = 8,
    SetWindowType = 9,
    TabNavigationPathPrunedFromFront = 11,
    SetPinnedState = 12,
    SetExtensionAppID = 13,
    SetWindowBounds3 = 14,
    SetWindowAppName = 15,
    TabClosed = 16,
    WindowClosed = 17,
    SessionStorageAssociated = 19,
    SetActiveWindow = 20,
    LastActiveTime = 21,
    SetWindowWorkspace2 = 23,
    TabNavigationPathPruned = 24,
    SetTabGroup = 25,
    SetTabGroupMetadata2 = 27,
    SetTabGuid = 28,
    SetTabUserAgentOverride2 = 29,
    SetTabData = 30,
    SetWindowUserTitle = 31,
    SetWindowVisibleOnAllWorkspaces = 32,
    AddTabExtraData = 33,
    AddWindowExtraData = 34
};

struct SetTabWindow {
};

struct Unkown {
};

struct setTabIndexInWindow {
    s32 tabId;
    s32 index;
};

struct TabClosed {
    u32 windowId;
    u32 tabId;
    u64 closeTime;
};

struct WindowClosed {
};

struct UpdateTabNavigationPathPrunedFromBack {
};

struct UpdateTabNavigation {
};

struct SetSelectedNavigationIndex {
};

struct SetSelectedTabIndex {
};

struct SetWindowType {
    u32 windowId;
    u32 windowType;
};

struct TabNavigationPathPrunedFromFront {
};

struct SetPinnedState {
};

struct SetExtensionAppID {
};

struct SetWindowBounds3 {
    u32 windowId;
    u32 windowX;
    u32 windowY;
    u32 windowWidth;
    u32 windowHeight;
    u32 windowState;
};

struct SetWindowWorkspace2 {
    u32 windowId;
    str workspaceGuid;
    // TODO: flag Workspace String object
    // workspaceGuid;
};

struct LastActiveTime {
    u32 windowId;
    u32 tabId;
    s64 lastActiveTime;
};


namespace snss_command {
    
    struct command_contents {    
        u16 size;    
        command_type command;
        if (command == command_type::SetWindowBounds3) {
            SetWindowBounds3 windowBounds;
        } else if (command == command_type::SetWindowType) {
            SetWindowType windowType; 
        } else if (command == command_type::LastActiveTime) {
            LastActiveTime lastActiveTime;
        } else if (command == command_type::TabClosed ) {
            TabClosed tabClosed;
        // Set WindowWorkspace2 is not fully implemented above
        /*} else if (command == command_type::SetWindowWorkspace2) {
            SetWindowWorkspace2 windowWorkspace; */
        } else {
        // Any undefined commands fall here
        // An array of [size - 1] highlights the size of the command
        // minus the command_type.
            u8 undefined[size - 1]; 
        }
         
    };
    struct command {   
        command_contents contents ;       
    };
    
}


struct snss_hdr_t {
    u32 magic_number; 
    u32 version_major;
    // TODO: calculate the number of commands in the file
    snss_command::command c[100];
};

snss_hdr_t snss @ 0x00;



