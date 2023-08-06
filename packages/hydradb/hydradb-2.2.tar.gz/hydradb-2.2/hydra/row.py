class Row:
    def __init__(self, connection):
        """
        Insert, delete, modify, or retrieve a row.

        Note:
            Aggregate or use composition while using
            this class in another object. Also, make sure to
            pass the connection object as a parameter.

        Examples:
            >>> self.row = Row('pass connection obj')

        Args:
            connection (:obj:`Connection`): Connect to the database.

        Attributes:
            self.__con (:obj:`Connection`): Use composition for connection.
        """

        self.__con = connection

    def __str__(self):
        """
        String representation of the Row class.

        Note:
            Use this in a print statement to print the
            documentation of the constructor.

        Returns:
            Returns the constructor documentation as string.
        """

        return self.__init__.__doc__

    def insert(self, table, **data):
        """
        Insert data in a table.

        Notes:
            Pass the table name in the first parameter and
            pass a **kwargs type in the second parameter.

        Examples:
            >>> self.insert('tbl', col1='text', col2='integer')

        Args:
            table (str): Insert given data in this table.
            **data (:obj:`kwargs`): Insert this data in the given table.

        Keyword Args:
            **data (:obj:`kwargs`): Add the given data.
                The first part in key='val' represents the column
                name and the next part represents data type.

        Returns:
            Returns nothing.
        """

        # get column names join them using comma
        columns = ', '.join(data.keys())

        # get the values for columns as string
        values = str(list(data.values()))[1:-1]

        # query for inserting data in a table
        query = f'''
           INSERT INTO {table} ({columns})
           VALUES ({values})
        ;'''

        # execute the query
        self.__con.execute(query)

    def delete(self, table, row_id):
        """
        Delete a row from a table.

        Note:
            Pass the table name in the first parameter and
            the primary key in the second parameter.

        Examples:
            >>> self.delete('tbl', 1)

        Args:
            table (str): Delete row from this table.
            row_id (int): Delete row with this primary key.

        Returns:
            Returns nothing.
        """

        # structure of the primary key
        primary_key = f"{table}_id"

        # query for deleting a row from a table
        query = f'''
           delete from {table}
           where {primary_key} = {row_id}
        ;'''

        # execute the query
        self.__con.execute(query)

    def update(self, table, row_id, **data):
        """
        Update a row in a table.

        Note:
            Pass the table name in the first parameter and
            pass the primary key in the second one. Also,
            the datatype for the third parameter is '**kwargs'.
            The first pair in the third parameter represents
            the column name and the second pair represents the
            value for that column.

        Examples:
            >>> self.update('tbl', 1, name='R', age='25')

        Args:
            table (str): Update a row from this table.
            row_id (int): Update a row with this id.
            **data (:obj:`kwargs`): Update a row with this data.

        Keyword Args:
            **data (:obj:`kwargs`): Update with the given data.
                First part in key='val' represents the column name
                and the next part represents data.

        Returns:
            Returns nothing.
        """

        # store columns and their values
        column_value = "".join(f"{col}='{val}'," for (col, val) in data.items())[0:-1]

        # structure for primary key
        primary_key = f"{table}_id"

        # query for updating row(s) in a table
        query = f'''
            UPDATE {table}
            SET {column_value}
            WHERE {primary_key} = {row_id}
        ;'''

        # execute the query
        self.__con.execute(query)
