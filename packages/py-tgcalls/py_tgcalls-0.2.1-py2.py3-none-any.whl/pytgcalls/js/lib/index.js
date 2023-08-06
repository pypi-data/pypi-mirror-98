"use strict";
var __classPrivateFieldSet = (this && this.__classPrivateFieldSet) || function (receiver, privateMap, value) {
    if (!privateMap.has(receiver)) {
        throw new TypeError("attempted to set private field on non-instance");
    }
    privateMap.set(receiver, value);
    return value;
};
var __classPrivateFieldGet = (this && this.__classPrivateFieldGet) || function (receiver, privateMap) {
    if (!privateMap.has(receiver)) {
        throw new TypeError("attempted to get private field on non-instance");
    }
    return privateMap.get(receiver);
};
var _connection, _params, _source_id;
Object.defineProperty(exports, "__esModule", { value: true });
exports.TGCalls = exports.Stream = void 0;
const events_1 = require("events");
const wrtc_1 = require("wrtc");
const sdp_builder_1 = require("./sdp-builder");
const utils_1 = require("./utils");
var stream_1 = require("./stream");
Object.defineProperty(exports, "Stream", { enumerable: true, get: function () { return stream_1.Stream; } });
class TGCalls extends events_1.EventEmitter {
    constructor(params) {
        super();
        _connection.set(this, void 0);
        _params.set(this, void 0);
        _source_id.set(this, 0);
        __classPrivateFieldSet(this, _params, params);
    }
    async start(track) {
        if (__classPrivateFieldGet(this, _connection)) {
            throw new Error('Connection already started');
        }
        else if (!this.joinVoiceCall) {
            throw new Error('Please set the `joinVoiceCall` callback before calling `start()`');
        }
        __classPrivateFieldSet(this, _connection, new wrtc_1.RTCPeerConnection());
        __classPrivateFieldGet(this, _connection).oniceconnectionstatechange = async () => {
            var _a, _b;
            this.emit('iceConnectionState', (_a = __classPrivateFieldGet(this, _connection)) === null || _a === void 0 ? void 0 : _a.iceConnectionState);
            switch ((_b = __classPrivateFieldGet(this, _connection)) === null || _b === void 0 ? void 0 : _b.iceConnectionState) {
                case 'closed':
                case 'failed':
                    this.emit('hangUp');
                    break;
            }
        };
        __classPrivateFieldGet(this, _connection).addTrack(track);
        const offer = await __classPrivateFieldGet(this, _connection).createOffer({
            offerToReceiveVideo: false,
            offerToReceiveAudio: true,
        });
        await __classPrivateFieldGet(this, _connection).setLocalDescription(offer);
        if (!offer.sdp) {
            return false;
        }
        const { ufrag, pwd, hash, fingerprint, source } = utils_1.parseSdp(offer.sdp);
        if (!ufrag || !pwd || !hash || !fingerprint || !source) {
            return false;
        }
        __classPrivateFieldSet(this, _source_id, source);
        const { transport } = await this.joinVoiceCall({
            ufrag,
            pwd,
            hash,
            setup: 'active',
            fingerprint,
            source,
            params: __classPrivateFieldGet(this, _params),
        });
        if (transport === null) {
            __classPrivateFieldGet(this, _connection).close();
            throw new Error('No transport found');
        }
        const sessionId = Date.now();
        const conference = {
            sessionId,
            transport,
            ssrcs: [{ ssrc: source, isMain: true }],
        };
        await __classPrivateFieldGet(this, _connection).setRemoteDescription({
            type: 'answer',
            sdp: sdp_builder_1.SdpBuilder.fromConference(conference, true),
        });
        return true;
    }
    getSignSource() {
        return __classPrivateFieldGet(this, _source_id);
    }
    close() {
        var _a;
        (_a = __classPrivateFieldGet(this, _connection)) === null || _a === void 0 ? void 0 : _a.close();
        __classPrivateFieldSet(this, _connection, undefined);
    }
}
exports.TGCalls = TGCalls;
_connection = new WeakMap(), _params = new WeakMap(), _source_id = new WeakMap();
