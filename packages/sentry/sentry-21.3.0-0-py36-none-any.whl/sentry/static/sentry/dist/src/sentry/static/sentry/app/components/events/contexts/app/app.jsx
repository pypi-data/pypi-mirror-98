import { __read, __spread } from "tslib";
import React from 'react';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import getUnknownData from '../getUnknownData';
import getAppKnownData from './getAppKnownData';
import { AppKnownDataType } from './types';
var appKnownDataValues = [
    AppKnownDataType.ID,
    AppKnownDataType.START_TIME,
    AppKnownDataType.DEVICE_HASH,
    AppKnownDataType.IDENTIFIER,
    AppKnownDataType.NAME,
    AppKnownDataType.VERSION,
    AppKnownDataType.BUILD,
];
var appIgnoredDataValues = [];
var App = function (_a) {
    var data = _a.data, event = _a.event;
    return (<React.Fragment>
    <ContextBlock data={getAppKnownData(event, data, appKnownDataValues)}/>
    <ContextBlock data={getUnknownData(data, __spread(appKnownDataValues, appIgnoredDataValues))}/>
  </React.Fragment>);
};
export default App;
//# sourceMappingURL=app.jsx.map