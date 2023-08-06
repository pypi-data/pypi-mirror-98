import asyncio


def start_ssl_proxy(port, target, target_ssl=False):
    import pproxy
    from localstack.services.generic_proxy import GenericProxy

    if ':' not in str(target):
        target = '127.0.0.1:%s' % target
    print('Starting SSL proxy server %s -> %s' % (port, target))

    # create server and remote connection
    server = pproxy.Server('secure+tunnel://0.0.0.0:%s' % port)
    target_proto = 'secure+tunnel' if target_ssl else 'tunnel'
    remote = pproxy.Connection('%s://%s' % (target_proto, target))
    args = dict(rserver=[remote], verbose=print)

    # set SSL contexts
    _, cert_file_name, key_file_name = GenericProxy.create_ssl_cert()
    for context in pproxy.server.sslcontexts:
        context.load_cert_chain(cert_file_name, key_file_name)

    loop = asyncio.get_event_loop()
    handler = loop.run_until_complete(server.start_server(args))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('exit!')

    handler.close()
    loop.run_until_complete(handler.wait_closed())
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
