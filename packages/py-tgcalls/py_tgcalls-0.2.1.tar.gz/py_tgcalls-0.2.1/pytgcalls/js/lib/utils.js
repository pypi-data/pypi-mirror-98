"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseSdp = void 0;
function parseSdp(sdp) {
    var _a, _b, _c, _d;
    let lines = sdp.split('\r\n');
    let lookup = (prefix) => {
        for (let line of lines) {
            if (line.startsWith(prefix)) {
                return line.substr(prefix.length);
            }
        }
        return null;
    };
    let rawSource = lookup('a=ssrc:');
    return {
        fingerprint: (_b = (_a = lookup('a=fingerprint:')) === null || _a === void 0 ? void 0 : _a.split(' ')[1]) !== null && _b !== void 0 ? _b : null,
        hash: (_d = (_c = lookup('a=fingerprint:')) === null || _c === void 0 ? void 0 : _c.split(' ')[0]) !== null && _d !== void 0 ? _d : null,
        setup: lookup('a=setup:'),
        pwd: lookup('a=ice-pwd:'),
        ufrag: lookup('a=ice-ufrag:'),
        source: rawSource ? parseInt(rawSource.split(' ')[0]) : null,
    };
}
exports.parseSdp = parseSdp;
