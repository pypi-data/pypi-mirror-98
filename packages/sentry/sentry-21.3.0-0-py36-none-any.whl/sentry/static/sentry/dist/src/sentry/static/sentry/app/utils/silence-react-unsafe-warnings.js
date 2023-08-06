import { __read, __spread } from "tslib";
// eslint-disable-next-line no-console
export var originalConsoleWarn = console.warn;
var REACT_UNSAFE_WARNING_REGEX = /componentWill.* has been renamed, and is not recommended for use.*/;
window.console.warn = function (message) {
    var args = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        args[_i - 1] = arguments[_i];
    }
    if (typeof message === 'string' && REACT_UNSAFE_WARNING_REGEX.test(message)) {
        return;
    }
    originalConsoleWarn.apply(void 0, __spread([message], args));
};
export var silencedWarn = window.console.warn;
//# sourceMappingURL=silence-react-unsafe-warnings.js.map