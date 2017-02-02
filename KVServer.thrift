namespace cpp KVStore
namespace d KVStore
namespace java KVStore
namespace perl KVStore
namespace php KVStore
namespace haxe KVStore

struct KVMessage{

  1: required map<string,string> value,
  // 2: required i32 id

}

exception KVException{

  1:string why

}


service KVInterface{

  void ping(),

  KVMessage set_element(1:string key, 2:string value) throws (1:KVException error),

  bool del_element(1:string key) throws (1: KVException error),

  string get_element(1:string key) throws (1:KVException error),

  list<string> list_elements();

}

struct KVCollection{

  1:list<KVMessage> elements

}

// typedef map<string,string> KVMessage;
//
// typedef list<KVMessage> KVCollection
