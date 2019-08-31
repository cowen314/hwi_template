from source.messaging import PubSubMessageCenter

if __name__ == "__main__":
    def listener(test_arg):
        print("An event occurred, this is being printed from the callback. Data: %s" % test_arg)
    PubSubMessageCenter.subscribe(listener, "test")
    PubSubMessageCenter.send_message("test", test_arg=123)
    pass
