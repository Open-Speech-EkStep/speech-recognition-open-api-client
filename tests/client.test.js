const StreamingClient = require('../src/client.js')
jest.mock("socket.io-client");
const origSocketClient = require('socket.io-client');
const flushPromises = require("flush-promises");
require('jest-fetch-mock').enableMocks()


describe('test streaming', function () {

    afterEach(() => {
        jest.resetAllMocks();
    });

    const socketOnMock = jest.fn();
    const socketDisconnectMock = jest.fn();

    beforeEach(() => {
        origSocketClient.mockImplementation(() => {
            const res = {};
            res.connect = jest.fn();
            res.on = socketOnMock;
            res.disconnect = socketDisconnectMock;
            return res;
        });
    })

    it('should have default values set', function () {
        const client = new StreamingClient();

        expect(client.language).toBe('en-IN');
        expect(client.defaultSampleRate).toBe(48000);
        expect(client.bufferSize).toBe(16384);
    });

    describe('connect', function () {

        it('should enable streaming', function () {
            const socketURL = "abc.com";
            const transcription_language = "hi";
            const onSuccessMock = jest.fn();
            const onErrorMock = jest.fn();

            const client = new StreamingClient();
            client.connect(socketURL, transcription_language, onSuccessMock, onErrorMock);

            expect(client.language).toBe(transcription_language);
            expect(origSocketClient.connect).toHaveBeenCalledTimes(1)
            expect(socketOnMock).toHaveBeenCalledTimes(5)
        });
    });

    describe('disconnect', function () {
        it('should enable streaming', function () {

            const client = new StreamingClient();

            client.connect();
            client.disconnect()

            expect(socketDisconnectMock).toHaveBeenCalledTimes(1)
        });
    });

});

describe('punctuateText', () => {
    beforeAll(() => {
        global.FormData = FormDataMock

        function FormDataMock() {
            this.append = jest.fn();
        }
    });

    beforeEach(() => {
        jest.resetAllMocks();
    })

    it('should call success callback', async function () {
        fetchMock.mockOnce('{"data": {"text": "hello", "language": "en-in"}}');


        const client = new StreamingClient();
        const onSuccess = jest.fn();
        const onError = jest.fn();

        client.punctuateText("hello", "abc.com", onSuccess, onError)
        await flushPromises();
        expect(onSuccess).toHaveBeenLastCalledWith(200, 'hello');
        expect(onError).not.toBeCalled();
    });

    it('should call error callback', async function () {
        const error = new Error('failed to get response');
        fetchMock.mockRejectOnce(error)


        const client = new StreamingClient();
        const onSuccess = jest.fn();
        const onError = jest.fn();

        client.punctuateText("hello", "abc.com", onSuccess, onError)
        await flushPromises();
        expect(onError).toHaveBeenLastCalledWith(undefined, error);
        expect(onSuccess).not.toHaveBeenCalled();
    });

    it('should return without callback when not callback provided', async function () {
        const error = new Error('failed to get response');
        fetchMock.mockRejectOnce(error)

        const client = new StreamingClient();

        client.punctuateText("hello", "abc.com")
        await flushPromises();
        expect(fetchMock).toHaveBeenCalledTimes(1)
    });

    it('should not make api call when text is undefined', async function () {
        const error = new Error('failed to get response');
        fetchMock.mockRejectOnce(error)


        const client = new StreamingClient();
        const onSuccess = jest.fn();
        const onError = jest.fn();

        client.punctuateText(undefined, "abc.com", onSuccess, onError);
        await flushPromises();
        expect(onError).toHaveBeenCalledWith(400, "Text cannot be empty.");
        expect(onSuccess).not.toHaveBeenCalled();
        expect(fetchMock).not.toHaveBeenCalled();
    });
});