import { t } from 'app/locale';
import { DebugFileFeature, DebugFileType } from 'app/types/debugFiles';
export function getFileType(dsym) {
    var _a;
    switch ((_a = dsym.data) === null || _a === void 0 ? void 0 : _a.type) {
        case DebugFileType.EXE:
            return t('executable');
        case DebugFileType.DBG:
            return t('debug companion');
        case DebugFileType.LIB:
            return t('dynamic library');
        default:
            return null;
    }
}
export function getFeatureTooltip(feature) {
    switch (feature) {
        case DebugFileFeature.SYMTAB:
            return t('Symbol tables are used as a fallback when full debug information is not available');
        case DebugFileFeature.DEBUG:
            return t('Debug information provides function names and resolves inlined frames during symbolication');
        case DebugFileFeature.UNWIND:
            return t('Stack unwinding information improves the quality of stack traces extracted from minidumps');
        case DebugFileFeature.SOURCES:
            return t('Source code information allows Sentry to display source code context for stack frames');
        default:
            return null;
    }
}
//# sourceMappingURL=utils.jsx.map