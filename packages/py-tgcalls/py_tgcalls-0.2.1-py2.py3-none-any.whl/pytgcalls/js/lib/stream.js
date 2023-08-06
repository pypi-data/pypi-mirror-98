"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Stream = void 0;
const events_1 = require("events");
const wrtc_1 = require("wrtc");
class Stream extends events_1.EventEmitter {
    constructor(readable, bitsPerSample = 16, sampleRate = 48000, channelCount = 1) {
        super();
        this.bitsPerSample = bitsPerSample;
        this.sampleRate = sampleRate;
        this.channelCount = channelCount;
        this._paused = false;
        this._finished = true;
        this._stopped = false;
        this.OnStreamEnd = Function;
        this._finishedLoading = false;
        this.audioSource = new wrtc_1.nonstandard.RTCAudioSource();
        this.cache = Buffer.alloc(0);
        this.setReadable(readable);
        this.processData();
    }
    setReadable(readable) {
        if (this._stopped) {
            throw new Error('Cannot set readable when stopped');
        }
        this.cache = Buffer.alloc(0);
        if (readable) {
            this._finished = false;
            this._finishedLoading = false;
            readable.on('data', data => {
                this.cache = Buffer.concat([this.cache, data]);
            });
            readable.on('end', () => {
                this._finishedLoading = true;
            });
        }
    }
    pause() {
        if (this._stopped) {
            throw new Error('Cannot pause when stopped');
        }
        this._paused = true;
        this.emit('pause', this._paused);
    }
    resume() {
        if (this._stopped) {
            throw new Error('Cannot resume when stopped');
        }
        this._paused = false;
        this.emit('resume', this._paused);
    }
    get paused() {
        return this._paused;
    }
    finish() {
        this._finished = true;
    }
    get finished() {
        return this._finished;
    }
    stop() {
        this.finish();
        this._stopped = true;
    }
    get stopped() {
        return this._stopped;
    }
    createTrack() {
        return this.audioSource.createTrack();
    }
    getIdSource() {
        return this.audioSource;
    }
    processData() {
        if (this._stopped) {
            return;
        }
        const byteLength = ((this.sampleRate * this.bitsPerSample) / 8 / 100) * this.channelCount;
        if (!this._paused && !this._finished && (this.cache.length >= byteLength || this._finishedLoading)) {
            const buffer = this.cache.slice(0, byteLength);
            const samples = new Int16Array(new Uint8Array(buffer).buffer);
            this.cache = this.cache.slice(byteLength);
            try {
                this.audioSource.onData({
                    bitsPerSample: this.bitsPerSample,
                    sampleRate: this.sampleRate,
                    channelCount: this.channelCount,
                    numberOfFrames: samples.length,
                    samples,
                });
            }
            catch (error) {
                this.emit('error', error);
            }
        }
        if (!this._finished && this._finishedLoading && this.cache.length < byteLength) {
            this.finish();
            if (this.OnStreamEnd !== Function) {
                this.OnStreamEnd();
            }
            this.emit('finish');
        }
        setTimeout(() => this.processData(), this._finished || this._paused ? 500 : 10);
    }
}
exports.Stream = Stream;
