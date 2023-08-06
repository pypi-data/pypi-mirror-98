try:
    import configparser as ConfigParser
except:
    import ConfigParser
import io
import os
import errno

from six.moves import input


class ConnectionConfig(dict):
    """Loads or creates .cfg file to/from object

    Config properties can be accessed as attributes or as dictionary keys.
    Treating object as dict only contains config items, not special properties.
    """

    properties = ("path", "server")

    def __init__(self, server, path=None, **kwargs):
        """
        Args:
            server (str): Name of server section in config file
            path (str, optional): Path to config file
        """
        self.server = server

        self.path = path
        if path:
            self.load_from_file(path=path)

    def load_from_file(self, path=None, stream=None):
        """Loads config file

        Args:
            path (str, optional): Path to file. specifiying this also updates the
                `path` property of the ConnectionConfig instance.
            stream (optional): Text stream of config.
        """
        config = ConfigParser.ConfigParser()
        if path and stream:
            raise IOError("Cannot pass both path and stream")

        if not os.path.exists(path):
            with open(path, "w") as fid:
                pass

        if path:
            config.readfp(open(path))
        elif stream:
            config.readfp(io.BytesIO(stream))

        self.path = path
        self.update({t[0]: t[1] for t in config.items(self.server)})

        return self

    def save(self, path=None):
        """Saves section to config file

        Args:
            path (str, optional): Path to save file instead of object's
                 `path` property. Does NOT change `path` property.
        """
        path = path if path else self.path
        config = ConfigParser.ConfigParser()

        if path:
            try:
                config.readfp(open(path))
            except IOError as e:
                if not e.errno == errno.ENOENT:
                    raise

        try:
            config.add_section(self.server)
        except ConfigParser.DuplicateSectionError as e:
            pass

        # Set server properties
        config.set(self.server, "url", self.url)

        if self.auth_url:
            config.set(self.server, "auth_url", self.auth_url)

        config.write(open(path, "w"))

        return self

    def save_config(self, path=None):
        """Prompts for user input, if needed, before calling save()

        Args:
            path (str, optional): Save location to use instead of `path` property.
        """
        path = path if path else self.path

        self.url = self.url or input("Enter server URL: ")

        if self.url[-1] != "/":
            self.url += "/"

        self.auth_url = self.url + "oauth/"

        config = self.save(path)

        print(
            "Saved configuration file to {}".format(
                os.path.join(os.path.abspath("."), path)
            )
        )

        return self

    def get_server_dict(self):
        return self

    def create_config_object(self, path=None, url=None, auth_url=None):
        """Creates new config section if needed
        """
        path = path if path else self.path

        self.url = url
        self.auth_url = auth_url

        if not path:
            path = input("Enter name of config file (connect.cfg): ") or "connect.cfg"
        self.save_config()

        return self

    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, key, value):
        super(ConnectionConfig, self).__setattr__(key, value)
        if key in self.properties:
            return
        try:
            super(ConnectionConfig, self).__setitem__(key, value)
        except KeyError as e:
            raise AttributeError(e)

    def __setitem__(self, key, value):
        if key in self.properties:
            raise KeyError("This key is reserved by the system.")
        super(ConnectionConfig, self).__setitem__(key, value)
        try:
            super(ConnectionConfig, self).__setattr__(key, value)
        except AttributeError as e:
            raise KeyError(e)

    def __delattr__(self, key):
        super(ConnectionConfig, self).__delattr__(key)
        try:
            super(ConnectionConfig, self).__delitem__(key)
        except KeyError as e:
            raise AttributeError(e)

    def __delitem__(self, key):
        super(ConnectionConfig, self).__delitem__(key)
        try:
            super(ConnectionConfig, self).__delattr__(key)
        except AttributeError as e:
            raise KeyError(e)
