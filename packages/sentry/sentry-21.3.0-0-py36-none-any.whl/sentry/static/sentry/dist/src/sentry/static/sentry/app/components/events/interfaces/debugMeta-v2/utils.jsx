import { ImageStatus } from 'app/types/debugImage';
export var IMAGE_AND_CANDIDATE_LIST_MAX_HEIGHT = 400;
export function getStatusWeight(status) {
    switch (status) {
        case null:
        case undefined:
        case ImageStatus.UNUSED:
            return 0;
        case ImageStatus.FOUND:
            return 1;
        default:
            return 2;
    }
}
export function combineStatus(debugStatus, unwindStatus) {
    var debugWeight = getStatusWeight(debugStatus);
    var unwindWeight = getStatusWeight(unwindStatus);
    var combined = debugWeight >= unwindWeight ? debugStatus : unwindStatus;
    return combined || ImageStatus.UNUSED;
}
export function getFileName(path) {
    if (!path) {
        return undefined;
    }
    var directorySeparator = /^([a-z]:\\|\\\\)/i.test(path) ? '\\' : '/';
    return path.split(directorySeparator).pop();
}
export function normalizeId(id) {
    var _a;
    return (_a = id === null || id === void 0 ? void 0 : id.trim().toLowerCase().replace(/[- ]/g, '')) !== null && _a !== void 0 ? _a : '';
}
//# sourceMappingURL=utils.jsx.map