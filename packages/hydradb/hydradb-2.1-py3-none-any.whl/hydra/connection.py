import sqlite3
from hydra.file import File


class Connection:
    def __init__(self, name=None, location=None):
        """
        Connect to the database file using a given name and location.

        Note:
            Leave the parameters empty if you want to connect to a file
            in the working directory. The default for the name is 'main'.
            If an SQLite '.db' file in the desired location is not present,
            it will create it.

        Examples:
            >>> self.conn = Connection('name', 'location')

        Args:
            name (str, optional): Connect to the file with this name.
                If the name is empty, it will connect to the 'main' file.

            location (str, optional): Connect to the file in this
                location. If location is empty, it will connect to a file
                in the working directory.

        Attributes:
            self.db_file (:obj:`str`): Store full directory address of the file.
        """

        # full directory address of the file
        self.__db_file = str(File(name, location))

        # create/connect to the database file
        self.execute("")

    def __str__(self):
        """
        String representation of the Connection class.

        Note:
            Use this in a print statement to print the
            documentation of the constructor.

        Returns:
            Returns the constructor documentation as string.
        """

        return self.__init__.__doc__

    def execute(self, query):
        """
        Connect to the '.db' file and execute a query.

        Note:
            Pass the query to execute it. If parameters are empty,
            it will only connect to the file.

        Examples:
            >>> self.execute("")
            >>> self.execute('select * from tbl')

        Args:
            query (str): Execute the given query.

        Returns:
            Returns the fetch result after executing a query.
        """

        # use context manager for connection
        with sqlite3.connect(self.__db_file) as con:
            # get the cursor from the connection
            cursor = con.cursor()

            # if query is given, execute it
            # otherwise, only connect to the file
            # if query:
            cursor.execute(query)

            # return the fetch result
            return cursor.fetchall()

    def fetch(self, query):
        """
        Execute a query and return the fetch result.

        Note:
            Use this function if you want the return
            value. Otherwise, use the execute() function.

        Args:
            query (str):

        Returns:
            Returns the fetch result after executing a query
        """
        return self.execute(query)
