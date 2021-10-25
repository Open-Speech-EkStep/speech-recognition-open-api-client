const {StreamingClient, SocketStatus} = require('../src/index');

describe('Module exports', function () {
    it('should export StreamingClient and SocketStatus', function () {
        expect(StreamingClient).toBeTruthy();
        expect(SocketStatus).toBeTruthy();
    });
});