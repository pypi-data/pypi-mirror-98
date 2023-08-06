import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import classNames from 'classnames';
import scrollToElement from 'scroll-to-element';
import Button from 'app/components/button';
import { combineStatus } from 'app/components/events/interfaces/debugMeta/utils';
import PackageLink from 'app/components/events/interfaces/packageLink';
import PackageStatus, { PackageStatusIcon, } from 'app/components/events/interfaces/packageStatus';
import TogglableAddress, { AddressToggleIcon, } from 'app/components/events/interfaces/togglableAddress';
import { SymbolicatorStatus } from 'app/components/events/interfaces/types';
import { STACKTRACE_PREVIEW_TOOLTIP_DELAY } from 'app/components/stacktracePreview';
import StrictClick from 'app/components/strictClick';
import { IconChevron, IconRefresh } from 'app/icons';
import { t } from 'app/locale';
import { DebugMetaActions } from 'app/stores/debugMetaStore';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { defined, objectIsEmpty } from 'app/utils';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withOrganization from 'app/utils/withOrganization';
import withSentryAppComponents from 'app/utils/withSentryAppComponents';
import Context from './context';
import DefaultTitle from './defaultTitle';
import Symbol, { FunctionNameToggleIcon } from './symbol';
import { getPlatform, isDotnet } from './utils';
function makeFilter(addr, addrMode, image) {
    if (!(!addrMode || addrMode === 'abs') && image) {
        return image.debug_id + "!" + addr;
    }
    return addr;
}
var Line = /** @class */ (function (_super) {
    __extends(Line, _super);
    function Line() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // isExpanded can be initialized to true via parent component;
        // data synchronization is not important
        // https://facebook.github.io/react/tips/props-in-getInitialState-as-anti-pattern.html
        _this.state = {
            isExpanded: _this.props.isExpanded,
        };
        _this.toggleContext = function (evt) {
            evt && evt.preventDefault();
            var _a = _this.props, isFirst = _a.isFirst, isHoverPreviewed = _a.isHoverPreviewed, organization = _a.organization;
            if (isFirst && isHoverPreviewed) {
                trackAnalyticsEvent({
                    eventKey: 'stacktrace.preview.first_frame_expand',
                    eventName: 'Stack Trace Preview: Expand First Frame',
                    organization_id: (organization === null || organization === void 0 ? void 0 : organization.id) ? parseInt(organization.id, 10) : undefined,
                    issue_id: _this.props.event.groupID,
                });
            }
            _this.setState({
                isExpanded: !_this.state.isExpanded,
            });
        };
        _this.scrollToImage = function (event) {
            event.stopPropagation(); // to prevent collapsing if collapsable
            var _a = _this.props.data, instructionAddr = _a.instructionAddr, addrMode = _a.addrMode;
            if (instructionAddr) {
                DebugMetaActions.updateFilter(makeFilter(instructionAddr, addrMode, _this.props.image));
            }
            scrollToElement('#images-loaded');
        };
        _this.preventCollapse = function (evt) {
            evt.stopPropagation();
        };
        return _this;
    }
    Line.prototype.hasContextSource = function () {
        return defined(this.props.data.context) && !!this.props.data.context.length;
    };
    Line.prototype.hasContextVars = function () {
        return !objectIsEmpty(this.props.data.vars || {});
    };
    Line.prototype.hasContextRegisters = function () {
        return !objectIsEmpty(this.props.registers);
    };
    Line.prototype.hasAssembly = function () {
        return isDotnet(this.getPlatform()) && defined(this.props.data.package);
    };
    Line.prototype.isExpandable = function () {
        return ((!this.props.isOnlyFrame && this.props.emptySourceNotation) ||
            this.hasContextSource() ||
            this.hasContextVars() ||
            this.hasContextRegisters() ||
            this.hasAssembly());
    };
    Line.prototype.getPlatform = function () {
        var _a;
        // prioritize the frame platform but fall back to the platform
        // of the stack trace / exception
        return getPlatform(this.props.data.platform, (_a = this.props.platform) !== null && _a !== void 0 ? _a : 'other');
    };
    Line.prototype.isInlineFrame = function () {
        return (this.props.prevFrame &&
            this.getPlatform() === (this.props.prevFrame.platform || this.props.platform) &&
            this.props.data.instructionAddr === this.props.prevFrame.instructionAddr);
    };
    Line.prototype.shouldShowLinkToImage = function () {
        var _a = this.props, isHoverPreviewed = _a.isHoverPreviewed, data = _a.data;
        var symbolicatorStatus = data.symbolicatorStatus;
        return (!!symbolicatorStatus &&
            symbolicatorStatus !== SymbolicatorStatus.UNKNOWN_IMAGE &&
            !isHoverPreviewed);
    };
    Line.prototype.packageStatus = function () {
        // this is the status of image that belongs to this frame
        var image = this.props.image;
        if (!image) {
            return 'empty';
        }
        var combinedStatus = combineStatus(image.debug_status, image.unwind_status);
        switch (combinedStatus) {
            case 'unused':
                return 'empty';
            case 'found':
                return 'success';
            default:
                return 'error';
        }
    };
    Line.prototype.renderExpander = function () {
        if (!this.isExpandable()) {
            return null;
        }
        var isHoverPreviewed = this.props.isHoverPreviewed;
        var isExpanded = this.state.isExpanded;
        return (<ToggleContextButtonWrapper>
        <ToggleContextButton className="btn-toggle" css={isDotnet(this.getPlatform()) && { display: 'block !important' }} // remove important once we get rid of css files
         title={t('Toggle Context')} tooltipProps={isHoverPreviewed ? { delay: STACKTRACE_PREVIEW_TOOLTIP_DELAY } : undefined} onClick={this.toggleContext}>
          <IconChevron direction={isExpanded ? 'up' : 'down'} size="8px"/>
        </ToggleContextButton>
      </ToggleContextButtonWrapper>);
    };
    Line.prototype.leadsToApp = function () {
        var _a = this.props, data = _a.data, nextFrame = _a.nextFrame;
        return !data.inApp && ((nextFrame && nextFrame.inApp) || !nextFrame);
    };
    Line.prototype.isFoundByStackScanning = function () {
        var data = this.props.data;
        return data.trust === 'scan' || data.trust === 'cfi-scan';
    };
    Line.prototype.renderLeadHint = function () {
        var isExpanded = this.state.isExpanded;
        if (isExpanded) {
            return null;
        }
        var leadsToApp = this.leadsToApp();
        if (!leadsToApp) {
            return null;
        }
        var nextFrame = this.props.nextFrame;
        return !nextFrame ? (<LeadHint className="leads-to-app-hint" width="115px">
        {t('Crashed in non-app: ')}
      </LeadHint>) : (<LeadHint className="leads-to-app-hint">{t('Called from: ')}</LeadHint>);
    };
    Line.prototype.renderRepeats = function () {
        var timesRepeated = this.props.timesRepeated;
        if (timesRepeated && timesRepeated > 0) {
            return (<RepeatedFrames title={"Frame repeated " + timesRepeated + " time" + (timesRepeated === 1 ? '' : 's')}>
          <RepeatedContent>
            <StyledIconRefresh />
            <span>{timesRepeated}</span>
          </RepeatedContent>
        </RepeatedFrames>);
        }
        return null;
    };
    Line.prototype.renderDefaultLine = function () {
        var _a;
        var isHoverPreviewed = this.props.isHoverPreviewed;
        return (<StrictClick onClick={this.isExpandable() ? this.toggleContext : undefined}>
        <DefaultLine className="title">
          <VertCenterWrapper>
            <div>
              {this.renderLeadHint()}
              <DefaultTitle frame={this.props.data} platform={(_a = this.props.platform) !== null && _a !== void 0 ? _a : 'other'} isHoverPreviewed={isHoverPreviewed}/>
            </div>
            {this.renderRepeats()}
          </VertCenterWrapper>
          {this.renderExpander()}
        </DefaultLine>
      </StrictClick>);
    };
    Line.prototype.renderNativeLine = function () {
        var _a = this.props, data = _a.data, showingAbsoluteAddress = _a.showingAbsoluteAddress, onAddressToggle = _a.onAddressToggle, onFunctionNameToggle = _a.onFunctionNameToggle, image = _a.image, maxLengthOfRelativeAddress = _a.maxLengthOfRelativeAddress, isFrameAfterLastNonApp = _a.isFrameAfterLastNonApp, includeSystemFrames = _a.includeSystemFrames, showCompleteFunctionName = _a.showCompleteFunctionName, isHoverPreviewed = _a.isHoverPreviewed;
        var leadHint = this.renderLeadHint();
        var packageStatus = this.packageStatus();
        return (<StrictClick onClick={this.isExpandable() ? this.toggleContext : undefined}>
        <DefaultLine className="title as-table">
          <NativeLineContent isFrameAfterLastNonApp={!!isFrameAfterLastNonApp}>
            <PackageInfo>
              {leadHint}
              <PackageLink includeSystemFrames={!!includeSystemFrames} withLeadHint={leadHint !== null} packagePath={data.package} onClick={this.scrollToImage} isClickable={this.shouldShowLinkToImage()} isHoverPreviewed={isHoverPreviewed}>
                {!isHoverPreviewed && (<PackageStatus status={packageStatus} tooltip={t('Go to Images Loaded')}/>)}
              </PackageLink>
            </PackageInfo>
            {data.instructionAddr && (<TogglableAddress address={data.instructionAddr} startingAddress={image ? image.image_addr : null} isAbsolute={!!showingAbsoluteAddress} isFoundByStackScanning={this.isFoundByStackScanning()} isInlineFrame={!!this.isInlineFrame()} onToggle={onAddressToggle} relativeAddressMaxlength={maxLengthOfRelativeAddress} isHoverPreviewed={isHoverPreviewed}/>)}
            <Symbol frame={data} showCompleteFunctionName={!!showCompleteFunctionName} onFunctionNameToggle={onFunctionNameToggle} isHoverPreviewed={isHoverPreviewed}/>
          </NativeLineContent>
          {this.renderExpander()}
        </DefaultLine>
      </StrictClick>);
    };
    Line.prototype.renderLine = function () {
        switch (this.getPlatform()) {
            case 'objc':
            // fallthrough
            case 'cocoa':
            // fallthrough
            case 'native':
                return this.renderNativeLine();
            default:
                return this.renderDefaultLine();
        }
    };
    Line.prototype.render = function () {
        var data = this.props.data;
        var className = classNames({
            frame: true,
            'is-expandable': this.isExpandable(),
            expanded: this.state.isExpanded,
            collapsed: !this.state.isExpanded,
            'system-frame': !data.inApp,
            'frame-errors': data.errors,
            'leads-to-app': this.leadsToApp(),
        });
        var props = { className: className };
        return (<StyledLi {...props}>
        {this.renderLine()}
        <Context frame={data} event={this.props.event} registers={this.props.registers} components={this.props.components} hasContextSource={this.hasContextSource()} hasContextVars={this.hasContextVars()} hasContextRegisters={this.hasContextRegisters()} emptySourceNotation={this.props.emptySourceNotation} hasAssembly={this.hasAssembly()} expandable={this.isExpandable()} isExpanded={this.state.isExpanded} isHoverPreviewed={this.props.isHoverPreviewed}/>
      </StyledLi>);
    };
    Line.defaultProps = {
        isExpanded: false,
        emptySourceNotation: false,
        isHoverPreviewed: false,
    };
    return Line;
}(React.Component));
export { Line };
export default withOrganization(withSentryAppComponents(Line, { componentType: 'stacktrace-link' }));
var RepeatedFrames = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-block;\n  border-radius: 50px;\n  padding: 1px 3px;\n  margin-left: ", ";\n  border-width: thin;\n  border-style: solid;\n  border-color: ", ";\n  color: ", ";\n  background-color: ", ";\n  white-space: nowrap;\n"], ["\n  display: inline-block;\n  border-radius: 50px;\n  padding: 1px 3px;\n  margin-left: ", ";\n  border-width: thin;\n  border-style: solid;\n  border-color: ", ";\n  color: ", ";\n  background-color: ", ";\n  white-space: nowrap;\n"])), space(1), function (p) { return p.theme.orange500; }, function (p) { return p.theme.orange500; }, function (p) { return p.theme.backgroundSecondary; });
var VertCenterWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var RepeatedContent = styled(VertCenterWrapper)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  justify-content: center;\n"], ["\n  justify-content: center;\n"])));
var PackageInfo = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  order: 2;\n  align-items: flex-start;\n  @media (min-width: ", ") {\n    order: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  order: 2;\n  align-items: flex-start;\n  @media (min-width: ", ") {\n    order: 0;\n  }\n"])), function (props) { return props.theme.breakpoints[0]; });
var NativeLineContent = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  flex: 1;\n  grid-gap: ", ";\n  grid-template-columns: ", " 1fr;\n  align-items: center;\n  justify-content: flex-start;\n\n  @media (min-width: ", ") {\n    grid-template-columns: ", " 117px 1fr auto;\n  }\n\n  @media (min-width: ", ") and (max-width: ", ") {\n    grid-template-columns: ", " 117px 1fr auto;\n  }\n"], ["\n  display: grid;\n  flex: 1;\n  grid-gap: ", ";\n  grid-template-columns: ", " 1fr;\n  align-items: center;\n  justify-content: flex-start;\n\n  @media (min-width: ", ") {\n    grid-template-columns: ", " 117px 1fr auto;\n  }\n\n  @media (min-width: ", ") and (max-width: ",
    ") {\n    grid-template-columns: ", " 117px 1fr auto;\n  }\n"])), space(0.5), function (p) { return (p.isFrameAfterLastNonApp ? '167px' : '117px'); }, function (props) { return props.theme.breakpoints[0]; }, function (p) { return (p.isFrameAfterLastNonApp ? '200px' : '150px'); }, function (props) { return props.theme.breakpoints[2]; }, function (props) {
    return props.theme.breakpoints[3];
}, function (p) { return (p.isFrameAfterLastNonApp ? '180px' : '140px'); });
var DefaultLine = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr auto;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr auto;\n  align-items: center;\n"])));
var StyledIconRefresh = styled(IconRefresh)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.25));
var LeadHint = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  ", "\n  max-width: ", "\n"], ["\n  ", "\n  max-width: ", "\n"])), overflowEllipsis, function (p) { return (p.width ? p.width : '67px'); });
var ToggleContextButtonWrapper = styled('span')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
// the Button's label has the padding of 3px because the button size has to be 16x16 px.
var ToggleContextButton = styled(Button)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  span:first-child {\n    padding: 3px;\n  }\n"], ["\n  span:first-child {\n    padding: 3px;\n  }\n"])));
var StyledLi = styled('li')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  ", " {\n    flex-shrink: 0;\n  }\n  :hover {\n    ", " {\n      visibility: visible;\n    }\n    ", " {\n      visibility: visible;\n    }\n    ", " {\n      visibility: visible;\n    }\n  }\n"], ["\n  ", " {\n    flex-shrink: 0;\n  }\n  :hover {\n    ", " {\n      visibility: visible;\n    }\n    ", " {\n      visibility: visible;\n    }\n    ", " {\n      visibility: visible;\n    }\n  }\n"])), PackageStatusIcon, PackageStatusIcon, AddressToggleIcon, FunctionNameToggleIcon);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=line.jsx.map