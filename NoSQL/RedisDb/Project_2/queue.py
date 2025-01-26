from redis import Redis


"""Notification  simulator """


class Queue:
    _instance = None  

    @classmethod
    def __new__(cls, *args, **kwargs):
        """
        Create a new instance of the Queue class or return the existing instance.
        
        This method ensures that only one instance of the Queue class is created (Singleton pattern).
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)  
        return cls._instance  

    def __init__(self, queue_name='default'):
        """
        Initialize the Queue instance with a Redis connection and a specified queue name.
        
        Args:
            queue_name (str): The name of the Redis list to be used as the queue. Defaults to 'default'.
        """
        self.connection = Redis() 
        self.queue_name = queue_name  

    def push(self, list_name, value):
        """
        Push a value onto the specified list in Redis and add the list name to the set of alerts.
        
        Args:
            list_name (str): The name of the list to which the value will be added.
            value: The value to be added to the list.
        """
        self.connection.sadd(self.queue_name, list_name)  
        self.connection.rpush(list_name, value)  

    def pop(self, list_name, lifo=True):
        """
        Pop a value from the specified list in Redis.
        
        Args:
            list_name (str): The name of the list from which to pop a value.
            lifo (bool): If True, use LIFO (Last In First Out) behavior; otherwise, use FIFO (First In First Out).
        
        Returns:
            The popped value from the specified list.
        """
        if lifo:
            return self.connection.rpop(list_name)  
        return self.connection.lpop(list_name)  
    def get_alerts(self):
        """
        Retrieve all alert list names stored in Redis.
        
        Returns:
            A set of alert list names associated with this queue.
        """
        return self.connection.smembers(self.queue_name)  

    def get_list_data(self, list_name):
        """
        Retrieve all data from a specified list in Redis and delete that list.
        
        Args:
            list_name (str): The name of the list from which to retrieve data.
        
        Returns:
            A list of values retrieved from the specified Redis list.
        """
        data = self.connection.lrange(list_name, 0, -1)  # Get all items from the list
        self.connection.delete(list_name)  
        return data  

    def get_all_data(self):
        """
        Retrieve and delete all data from all lists associated with this queue.
        
        Returns:
            A dictionary where keys are list names and values are lists of data retrieved from those lists.
        """
        data = dict()  
        for list_name in self.get_alerts():  
            data[list_name] = self.get_list_data(list_name)  

        return data  
