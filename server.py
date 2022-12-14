import logging
import asyncio
import sys
sys.path.insert(0, "..")
from asyncua import ua, Server
from asyncua.common.methods import uamethod
from utility.load_config import load_config
import random

config = load_config()

@uamethod
def func(parent, value):
    return value * 2


async def main():
    _logger = logging.getLogger('asyncua')
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint(config['ServerEndpoint'])

    # setup our own namespace, not really necessary but should as spec
    uri = config['URI']
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myobj = await server.nodes.objects.add_object(idx, 'MyObject')
    myvar = await myobj.add_variable(idx, 'Runtime', 0)
    
    temp = await myobj.add_variable(idx, 'Temp', 0)
    axis_x = await myobj.add_variable(idx, 'X-Axis-Pos', 0)
    axis_y = await myobj.add_variable(idx, 'Y-Axis-Pos', 0)
    axis_z = await myobj.add_variable(idx, 'Z-Axis-Pos', 0)
    
    # Set MyVariable to be writable by clients
    await myvar.set_writable()
    await server.nodes.objects.add_method(ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2), func, [ua.VariantType.Int64], [ua.VariantType.Int64])
    _logger.info('Starting server!')
    async with server:
        while True:
            await asyncio.sleep(1)
            new_val = await myvar.get_value() + 1
            _logger.info('Set value of %s to %.1f', myvar, new_val)
            temp_value = random.randrange(0, 100)
            x_value = random.randrange(0, 10)
            _logger.info('Set value of %s to %.1f', axis_x, x_value)
            y_value = random.randrange(0, 10)
            _logger.info('Set value of %s to %.1f', axis_y, y_value)
            z_value = random.randrange(0, 10)
            _logger.info('Set value of %s to %.1f', axis_z, z_value)
            await myvar.write_value(new_val)
            await temp.write_value(temp_value)
            await axis_x.write_value(x_value)
            await axis_y.write_value(y_value)
            await axis_z.write_value(z_value)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main(), debug=True)