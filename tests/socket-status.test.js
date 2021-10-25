const SocketStatus = require('../src/socket-status');

describe('Socket Status', function () {
    it('should export SocketStatus', function () {
        expect(SocketStatus).toBeTruthy();
        expect(SocketStatus.CONNECTED).toBeTruthy();
        expect(SocketStatus.TERMINATED).toBeTruthy();
    });

    it('should match when compared with same', function () {
        expect(SocketStatus.CONNECTED === SocketStatus.CONNECTED).toBeTruthy();
        expect(SocketStatus.TERMINATED == SocketStatus.TERMINATED).toBeTruthy();
    });

    it('should not return false when compared with different status', function () {
        expect(SocketStatus.CONNECTED === SocketStatus.TERMINATED).toEqual(false)
        expect(SocketStatus.TERMINATED == SocketStatus.CONNECTED).toEqual(false)
    });
});