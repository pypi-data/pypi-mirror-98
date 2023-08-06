import { __read, __spread } from "tslib";
import { EntryType } from 'app/types/event';
var NATIVE_PLATFORMS = ['cocoa', 'native'];
// Finds all frames in a given data blob and returns it's platforms
function getPlatforms(exceptionValue) {
    var _a, _b, _c, _d;
    var frames = (_a = exceptionValue === null || exceptionValue === void 0 ? void 0 : exceptionValue.frames) !== null && _a !== void 0 ? _a : [];
    var stacktraceFrames = (_d = (_c = (_b = exceptionValue) === null || _b === void 0 ? void 0 : _b.stacktrace) === null || _c === void 0 ? void 0 : _c.frames) !== null && _d !== void 0 ? _d : [];
    if (!frames.length && !stacktraceFrames.length) {
        return [];
    }
    return __spread(frames, stacktraceFrames).map(function (frame) { return frame.platform; })
        .filter(function (platform) { return !!platform; });
}
function getStackTracePlatforms(event, exceptionEntry) {
    var _a, _b, _c, _d, _e;
    // Fetch platforms in stack traces of an exception entry
    var exceptionEntryPlatforms = ((_a = exceptionEntry.data.values) !== null && _a !== void 0 ? _a : []).flatMap(getPlatforms);
    // Fetch platforms in an exception entry
    var stackTraceEntry = ((_c = (_b = event.entries.find(function (entry) { return entry.type === EntryType.STACKTRACE; })) === null || _b === void 0 ? void 0 : _b.data) !== null && _c !== void 0 ? _c : {});
    // Fetch platforms in an exception entry
    var stackTraceEntryPlatforms = Object.keys(stackTraceEntry).flatMap(function (key) {
        return getPlatforms(stackTraceEntry[key]);
    });
    // Fetch platforms in an thread entry
    var threadEntry = ((_e = (_d = event.entries.find(function (entry) { return entry.type === EntryType.THREADS; })) === null || _d === void 0 ? void 0 : _d.data.values) !== null && _e !== void 0 ? _e : []);
    // Fetch platforms in a thread entry
    var threadEntryPlatforms = threadEntry.flatMap(function (_a) {
        var stacktrace = _a.stacktrace;
        return getPlatforms(stacktrace);
    });
    return new Set(__spread(exceptionEntryPlatforms, stackTraceEntryPlatforms, threadEntryPlatforms));
}
// Checks whether an event indicates that it has an apple crash report.
export function isNativeEvent(event, exceptionEntry) {
    var platform = event.platform;
    if (platform && NATIVE_PLATFORMS[platform]) {
        return true;
    }
    var stackTracePlatforms = getStackTracePlatforms(event, exceptionEntry);
    return NATIVE_PLATFORMS.some(function (nativePlatform) { return stackTracePlatforms.has(nativePlatform); });
}
//  Checks whether an event indicates that it has an associated minidump.
export function isMinidumpEvent(exceptionEntry) {
    var _a;
    var data = exceptionEntry.data;
    return ((_a = data.values) !== null && _a !== void 0 ? _a : []).some(function (value) { var _a; return ((_a = value.mechanism) === null || _a === void 0 ? void 0 : _a.type) === 'minidump'; });
}
// Checks whether an event indicates that it has an apple crash report.
export function isAppleCrashReportEvent(exceptionEntry) {
    var _a;
    var data = exceptionEntry.data;
    return ((_a = data.values) !== null && _a !== void 0 ? _a : []).some(function (value) { var _a; return ((_a = value.mechanism) === null || _a === void 0 ? void 0 : _a.type) === 'applecrashreport'; });
}
//# sourceMappingURL=utils.jsx.map