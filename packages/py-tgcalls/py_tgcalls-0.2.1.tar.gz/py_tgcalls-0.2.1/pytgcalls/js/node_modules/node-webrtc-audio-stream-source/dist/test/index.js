"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const wrtc_1 = __importDefault(require("wrtc"));
const fs_1 = __importDefault(require("fs"));
const assert_1 = __importDefault(require("assert"));
const src_1 = __importDefault(require("../src"));
const rtcAudioStreamSource = new src_1.default();
const track = rtcAudioStreamSource.createTrack();
const sink = new wrtc_1.default.nonstandard.RTCAudioSink(track);
const audioFilePath = 'temp.wav';
if (fs_1.default.existsSync(audioFilePath)) {
    fs_1.default.unlinkSync(audioFilePath);
}
const writeStream = fs_1.default.createWriteStream(audioFilePath, { flags: 'a' });
sink.ondata = (data) => {
    writeStream.write(Buffer.from(data.samples.buffer));
};
const readStream = fs_1.default.createReadStream('test.wav');
rtcAudioStreamSource.addStream(readStream, 16, 48000, 1);
setTimeout(() => {
    readStream.close();
    track.stop();
    sink.stop();
    writeStream.close();
    const testBuffer = fs_1.default.readFileSync('test.wav');
    const tempBuffer = fs_1.default.readFileSync('temp.wav');
    assert_1.default.ok(testBuffer.slice(0, tempBuffer.length).equals(tempBuffer));
}, 2000);
//# sourceMappingURL=index.js.map