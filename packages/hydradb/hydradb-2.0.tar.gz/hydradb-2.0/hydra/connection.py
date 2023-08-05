import sqlite3
from sqlite3 import Error
from hydra.file import File


class Connection:
    def __init__(self, name=None, location=None):
        """
        Connect to the database file using a given name and location.

        Note:
            Leave the parameters empty if you want to connect to a file
            in the working directory. The default for name is 'main'.
            If a SQLite '.db' file in the desired location is not present,
            it will create it.

        Examples:
            >>> self.conn = Connection('name', 'location')

        Args:
            name (str, optional): Connect to the file with this name.
                If name is empty, it will connect 'main' file.

            location (str, optional): Connect to the file in this
                location. If location is empty, it will connect to a file
                in the working directory.

        Attributes:
            self.db_file (:obj:`str`): Store full directory address of the file.
        """

        # full directory address of the file
        self.__db_file = str(File(name, location))

        # create/connect to the database file
        self.execute()

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

    def execute(self, query=None, data=None):
        """
        Connect to the '.db' file and execute a query with/without data.

        Note:
            Pass the query with/without the data to execute it.
            If parameters are empty, it will only connect to the file.

        Examples:
            >>> self.execute()
            >>> self.execute('select * from tbl')
            >>> self.execute('query', 'col1', 'col2')

        Args:
            query (str, optional): Execute the given query.
            data (:obj:`list`, optional): Execute the query with this data.

        Returns:
            Returns the fetch result after executing a query.

        Raises:
            Raises an exception if the connection to the database is
            not successful or if there is a problem with the query or data.
        """

        # set connection and cursor to None
        connection = None
        cursor = None

        try:
            # connect to the database file or create it
            connection = sqlite3.connect(self.__db_file)

            # create a cursor from the connection
            cursor = connection.cursor()

            # only execute the query if data is not given
            if query is not None and data is None:
                cursor.execute(query)

            # execute the query and data if both are given
            elif query is not None and data is not None:
                cursor.execute(query, data)

        # raise an exception if there is any error
        except Error as e:
            print(f"Err: {e}")

        # run the following lines of codes anyway
        finally:
            if connection:
                # store the fetch result
                fetch_result = cursor.fetchall()

                # save/commit all the changes in database
                connection.commit()

                # close the connection
                connection.close()

                # return the fetch result at the end
                return fetch_result
