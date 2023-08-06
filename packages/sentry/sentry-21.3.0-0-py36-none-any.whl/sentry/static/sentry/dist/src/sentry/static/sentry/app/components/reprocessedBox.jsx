import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { BannerContainer, BannerSummary } from 'app/components/events/styles';
import Link from 'app/components/links/link';
import { IconCheckmark, IconClose } from 'app/icons';
import { t, tct, tn } from 'app/locale';
import space from 'app/styles/space';
import localStorage from 'app/utils/localStorage';
var ReprocessedBox = /** @class */ (function (_super) {
    __extends(ReprocessedBox, _super);
    function ReprocessedBox() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isBannerHidden: localStorage.getItem(_this.getBannerUniqueId()) === 'true',
        };
        _this.handleBannerDismiss = function () {
            localStorage.setItem(_this.getBannerUniqueId(), 'true');
            _this.setState({ isBannerHidden: true });
        };
        return _this;
    }
    ReprocessedBox.prototype.getBannerUniqueId = function () {
        var reprocessActivity = this.props.reprocessActivity;
        var id = reprocessActivity.id;
        return "reprocessed-activity-" + id + "-banner-dismissed";
    };
    ReprocessedBox.prototype.renderMessage = function () {
        var _a = this.props, orgSlug = _a.orgSlug, reprocessActivity = _a.reprocessActivity, groupCount = _a.groupCount, groupId = _a.groupId;
        var data = reprocessActivity.data;
        var eventCount = data.eventCount, oldGroupId = data.oldGroupId, newGroupId = data.newGroupId;
        var reprocessedEventsRoute = "/organizations/" + orgSlug + "/issues/?query=reprocessing.original_issue_id:" + oldGroupId;
        if (groupCount === 0) {
            return tct('All events in this issue were moved during reprocessing. [link]', {
                link: (<Link to={reprocessedEventsRoute}>
            {tn('See %s new event', 'See %s new events', eventCount)}
          </Link>),
            });
        }
        return tct('Events in this issue were successfully reprocessed. [link]', {
            link: (<Link to={reprocessedEventsRoute}>
          {newGroupId === Number(groupId)
                ? tn('See %s reprocessed event', 'See %s reprocessed events', eventCount)
                : tn('See %s new event', 'See %s new events', eventCount)}
        </Link>),
        });
    };
    ReprocessedBox.prototype.render = function () {
        var isBannerHidden = this.state.isBannerHidden;
        if (isBannerHidden) {
            return null;
        }
        var className = this.props.className;
        return (<BannerContainer priority="success" className={className}>
        <StyledBannerSummary>
          <IconCheckmark color="green300" isCircled/>
          <span>{this.renderMessage()}</span>
          <StyledIconClose color="green300" aria-label={t('Dismiss')} isCircled onClick={this.handleBannerDismiss}/>
        </StyledBannerSummary>
      </BannerContainer>);
    };
    return ReprocessedBox;
}(React.Component));
export default ReprocessedBox;
var StyledBannerSummary = styled(BannerSummary)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  & > svg:last-child {\n    margin-right: 0;\n    margin-left: ", ";\n  }\n"], ["\n  & > svg:last-child {\n    margin-right: 0;\n    margin-left: ", ";\n  }\n"])), space(1));
var StyledIconClose = styled(IconClose)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  cursor: pointer;\n"], ["\n  cursor: pointer;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=reprocessedBox.jsx.map