import React from 'react';
import isNil from 'lodash/isNil';
import CrashContent from 'app/components/events/interfaces/crashContent';
import Pill from 'app/components/pill';
import Pills from 'app/components/pills';
import { t } from 'app/locale';
var Content = function (_a) {
    var _b;
    var event = _a.event, projectId = _a.projectId, data = _a.data, stackView = _a.stackView, stackType = _a.stackType, newestFirst = _a.newestFirst, exception = _a.exception, stacktrace = _a.stacktrace, hasMissingStacktrace = _a.hasMissingStacktrace;
    return (<div className="thread">
    {data && (!isNil(data === null || data === void 0 ? void 0 : data.id) || !!(data === null || data === void 0 ? void 0 : data.name)) && (<Pills>
        {!isNil(data.id) && <Pill name={t('id')} value={String(data.id)}/>}
        {!!((_b = data.name) === null || _b === void 0 ? void 0 : _b.trim()) && <Pill name={t('name')} value={data.name}/>}
        <Pill name={t('was active')} value={data.current}/>
        <Pill name={t('errored')} className={data.crashed ? 'false' : 'true'}>
          {data.crashed ? t('yes') : t('no')}
        </Pill>
      </Pills>)}

    {hasMissingStacktrace ? (<div className="traceback missing-traceback">
        <ul>
          <li className="frame missing-frame">
            <div className="title">
              <i>{(data === null || data === void 0 ? void 0 : data.crashed) ? t('Thread Errored') : t('No or unknown stacktrace')}</i>
            </div>
          </li>
        </ul>
      </div>) : (<CrashContent event={event} stackType={stackType} stackView={stackView} newestFirst={newestFirst} projectId={projectId} exception={exception} stacktrace={stacktrace}/>)}
  </div>);
};
export default Content;
//# sourceMappingURL=content.jsx.map