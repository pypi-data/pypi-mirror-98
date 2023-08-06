import React from 'react';
import StacktraceContent from 'app/components/events/interfaces/stacktraceContent';
import { Panel } from 'app/components/panels';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import { STACK_VIEW } from 'app/types/stacktrace';
import { defined } from 'app/utils';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
var ExceptionStacktraceContent = function (_a) {
    var _b, _c;
    var stackView = _a.stackView, stacktrace = _a.stacktrace, chainedException = _a.chainedException, platform = _a.platform, newestFirst = _a.newestFirst, data = _a.data, expandFirstFrame = _a.expandFirstFrame, event = _a.event;
    if (!defined(stacktrace)) {
        return null;
    }
    if (stackView === STACK_VIEW.APP &&
        ((_b = stacktrace.frames) !== null && _b !== void 0 ? _b : []).filter(function (frame) { return frame.inApp; }).length === 0 &&
        !chainedException) {
        return (<Panel dashedBorder>
        <EmptyMessage icon={<IconWarning size="xs"/>} title={t('No app only stack trace has been found!')}/>
      </Panel>);
    }
    if (!data) {
        return null;
    }
    /**
     * Armin, Markus:
     * If all frames are in app, then no frame is in app.
     * This normally does not matter for the UI but when chained exceptions
     * are used this causes weird behavior where one exception appears to not have a stack trace.
     *
     * It is easier to fix the UI logic to show a non-empty stack trace for chained exceptions
     */
    return (<StacktraceContent data={data} expandFirstFrame={expandFirstFrame} includeSystemFrames={stackView === STACK_VIEW.FULL ||
        (chainedException && ((_c = stacktrace.frames) !== null && _c !== void 0 ? _c : []).every(function (frame) { return !frame.inApp; }))} platform={platform} newestFirst={newestFirst} event={event}/>);
};
export default ExceptionStacktraceContent;
//# sourceMappingURL=exceptionStacktraceContent.jsx.map