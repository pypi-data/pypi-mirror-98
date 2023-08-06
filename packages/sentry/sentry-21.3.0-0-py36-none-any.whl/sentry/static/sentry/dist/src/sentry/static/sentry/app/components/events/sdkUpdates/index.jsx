import React from 'react';
import Alert from 'app/components/alert';
import EventDataSection from 'app/components/events/eventDataSection';
import { IconUpgrade } from 'app/icons';
import { tct } from 'app/locale';
import getSdkUpdateSuggestion from 'app/utils/getSdkUpdateSuggestion';
var SdkUpdates = function (_a) {
    var event = _a.event;
    var sdkUpdates = event.sdkUpdates;
    var eventDataSectinContent = sdkUpdates
        .map(function (sdkUpdate, index) {
        var suggestion = getSdkUpdateSuggestion({ suggestion: sdkUpdate, sdk: event.sdk });
        if (!suggestion) {
            return null;
        }
        return (<Alert key={index} type="info" icon={<IconUpgrade />}>
          {tct('We recommend you [suggestion]', { suggestion: suggestion })}
        </Alert>);
    })
        .filter(function (alert) { return !!alert; });
    if (!eventDataSectinContent.length) {
        return null;
    }
    return (<EventDataSection title={null} type="sdk-updates">
      {eventDataSectinContent}
    </EventDataSection>);
};
export default SdkUpdates;
//# sourceMappingURL=index.jsx.map