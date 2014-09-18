@0xb6bb6d7a080b2e0e;

# Oberon Message Format

struct SequencedMessage {
  datatype @0 :UInt32; # better as an enum?
  msgtype @1 :UInt32;
  id @2 :UInt64;
  version @3 :UInt32;
  attributes @4 :AnyPointer;
  extended @5 :List(KVPair);

  struct KVPair {
    key @0 :UInt16;
    union {
      boolean @1 :Bool;
	  int8    @2 :Int8;
	  int16   @3 :Int16;
	  int32   @4 :Int32;
	  int64   @5 :Int64;
      uint8   @6 :UInt8;
      uint16  @7 :UInt16;
      uint32  @8 :UInt32;
      unit64  @9 :UInt64;
      float32 @10 :Float32;
      float64 @11 :Float64;
      text    @12 :Text;
      data    @13 :Data;
      null    @14 :Void;
      # TODO Lists
    }
  }
}
 
struct UnsequencedMessage {
  type @0 :MessageType;
  source @1 :Text;
  time @2 :Float64;

  enum MessageType {
    heartbeat @0;
  }

}
