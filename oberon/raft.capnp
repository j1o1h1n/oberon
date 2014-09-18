@0xb7c862555661180f;

# RAFT protocol datatype

# Invoked by leader to replicate log entries; also used as heartbeat
struct AppendEntries {
  
  # leader's term
  term @0 :UInt32;
  
  # so follower can redirect clients
  leaderId @1 :UInt32;

  # index of log entry immediately preceding new ones  
  prevLogIndex @2 :UInt32;

  # term of prevLogIndex entry
  prevLogTerm @3 :UInt32;

  # log entries to store (empty for heartbeat; may send more than one for efficiency) 
  union {
    entries @4 :List(Data);
    heartbeat @5 :Void;
  }

  #leader's commitIndex
  leaderCommit @6 :UInt32;
}

# Response to AppendEntries
struct AppendEntriesResponse {
  
  # currentTerm, for leader to update itself true if follower contained entry matching prevLogIndex and prevLogTerm  
  term @0 :UInt32;

  # true if follower contained entry matching prevLogIndex and prevLogTerm
  success @1 :Bool;

}
