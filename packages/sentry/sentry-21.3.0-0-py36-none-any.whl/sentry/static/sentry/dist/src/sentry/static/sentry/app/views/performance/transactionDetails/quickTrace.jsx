import { __assign } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import * as Sentry from '@sentry/react';
import DropdownLink from 'app/components/dropdownLink';
import ErrorBoundary from 'app/components/errorBoundary';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import Link from 'app/components/links/link';
import Placeholder from 'app/components/placeholder';
import Tooltip from 'app/components/tooltip';
import Truncate from 'app/components/truncate';
import { IconFire } from 'app/icons';
import { t, tn } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getShortEventId } from 'app/utils/events';
import { getDuration } from 'app/utils/formatters';
import { isTransaction, parseQuickTrace } from 'app/utils/performance/quickTrace/utils';
import Projects from 'app/utils/projects';
import { DropdownItem, DropdownItemSubContainer, EventNode, MetaData, QuickTraceContainer, SectionSubtext, StyledTruncate, TraceConnector, } from './styles';
import { generateMultiEventsTarget, generateSingleEventTarget, generateTraceTarget, } from './utils';
function handleTraceLink(organization) {
    trackAnalyticsEvent({
        eventKey: 'quick_trace.trace_id.clicked',
        eventName: 'Quick Trace: Trace ID clicked',
        organization_id: parseInt(organization.id, 10),
    });
}
export default function QuickTrace(_a) {
    var _b, _c, _d;
    var event = _a.event, location = _a.location, organization = _a.organization, _e = _a.quickTrace, isLoading = _e.isLoading, error = _e.error, trace = _e.trace, type = _e.type;
    // non transaction events are currently unsupported
    if (!isTransaction(event)) {
        return null;
    }
    var traceId = (_d = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id) !== null && _d !== void 0 ? _d : null;
    var traceTarget = generateTraceTarget(event, organization);
    var body = isLoading ? (<Placeholder height="27px"/>) : error || trace === null ? ('\u2014') : (<ErrorBoundary mini>
      <QuickTracePills event={event} quickTrace={{ type: type, trace: trace }} location={location} organization={organization}/>
    </ErrorBoundary>);
    return (<MetaData headingText={t('Quick Trace')} tooltipText={t('A minified version of the full trace.')} bodyText={body} subtext={traceId === null ? ('\u2014') : (<Link to={traceTarget} onClick={function () { return handleTraceLink(organization); }}>
            {t('Trace ID: %s', getShortEventId(traceId))}
          </Link>)}/>);
}
function singleEventHoverText(event) {
    return (<div>
      <Truncate value={event.transaction} maxLength={30} leftTrim trimRegex={/\.|\//g} expandable={false}/>
      <div>
        {getDuration(event['transaction.duration'] / 1000, event['transaction.duration'] < 1000 ? 0 : 2, true)}
      </div>
    </div>);
}
function QuickTracePills(_a) {
    var event = _a.event, quickTrace = _a.quickTrace, location = _a.location, organization = _a.organization;
    // non transaction events are currently unsupported
    if (!isTransaction(event)) {
        return null;
    }
    var parsedQuickTrace;
    try {
        parsedQuickTrace = parseQuickTrace(quickTrace, event);
    }
    catch (error) {
        Sentry.setTag('current.event_id', event.id);
        Sentry.captureException(new Error('Current event not in quick trace'));
        return <React.Fragment>{'\u2014'}</React.Fragment>;
    }
    var root = parsedQuickTrace.root, ancestors = parsedQuickTrace.ancestors, parent = parsedQuickTrace.parent, children = parsedQuickTrace.children, descendants = parsedQuickTrace.descendants, current = parsedQuickTrace.current;
    var nodes = [];
    if (root) {
        nodes.push(<EventNodeSelector key="root-node" location={location} organization={organization} events={[root]} text={t('Root')} hoverText={singleEventHoverText(root)} pad="right" nodeKey="root"/>);
        nodes.push(<TraceConnector key="root-connector"/>);
    }
    if (ancestors === null || ancestors === void 0 ? void 0 : ancestors.length) {
        var ancestorHoverText = ancestors.length === 1
            ? singleEventHoverText(ancestors[0])
            : t('View all ancestor transactions of this event');
        nodes.push(<EventNodeSelector key="ancestors-node" location={location} organization={organization} events={ancestors} text={tn('%s Ancestor', '%s Ancestors', ancestors.length)} hoverText={ancestorHoverText} extrasTarget={generateMultiEventsTarget(event, ancestors, organization, location, 'Ancestor')} pad="right" nodeKey="ancestors"/>);
        nodes.push(<TraceConnector key="ancestors-connector"/>);
    }
    if (parent) {
        nodes.push(<EventNodeSelector key="parent-node" location={location} organization={organization} events={[parent]} text={t('Parent')} hoverText={singleEventHoverText(parent)} pad="right" nodeKey="parent"/>);
        nodes.push(<TraceConnector key="parent-connector"/>);
    }
    nodes.push(<EventNodeSelector key="current-node" location={location} organization={organization} text={t('This Event')} events={[current]} pad="left" nodeKey="current"/>);
    if (children.length) {
        nodes.push(<TraceConnector key="children-connector"/>);
        var childHoverText = children.length === 1
            ? singleEventHoverText(children[0])
            : t('View all child transactions of this event');
        nodes.push(<EventNodeSelector key="children-node" location={location} organization={organization} events={children} text={tn('%s Child', '%s Children', children.length)} hoverText={childHoverText} extrasTarget={generateMultiEventsTarget(event, children, organization, location, 'Children')} pad="left" nodeKey="children"/>);
    }
    if (descendants === null || descendants === void 0 ? void 0 : descendants.length) {
        nodes.push(<TraceConnector key="descendants-connector"/>);
        var descendantHoverText = descendants.length === 1
            ? singleEventHoverText(descendants[0])
            : t('View all child descendants of this event');
        nodes.push(<EventNodeSelector key="descendants-node" location={location} organization={organization} events={descendants} text={tn('%s Descendant', '%s Descendants', descendants.length)} hoverText={descendantHoverText} extrasTarget={generateMultiEventsTarget(event, descendants, organization, location, 'Descendant')} pad="left" nodeKey="descendants"/>);
    }
    return <QuickTraceContainer>{nodes}</QuickTraceContainer>;
}
function handleNode(key, organization) {
    trackAnalyticsEvent({
        eventKey: 'quick_trace.node.clicked',
        eventName: 'Quick Trace: Node clicked',
        organization_id: parseInt(organization.id, 10),
        node_key: key,
    });
}
function handleDropdownItem(target, key, organization, extra) {
    trackAnalyticsEvent({
        eventKey: 'quick_trace.dropdown.clicked' + (extra ? '_extra' : ''),
        eventName: 'Quick Trace: Dropdown clicked',
        organization_id: parseInt(organization.id, 10),
        node_key: key,
    });
    ReactRouter.browserHistory.push(target);
}
function EventNodeSelector(_a) {
    var location = _a.location, organization = _a.organization, _b = _a.events, events = _b === void 0 ? [] : _b, text = _a.text, pad = _a.pad, hoverText = _a.hoverText, extrasTarget = _a.extrasTarget, nodeKey = _a.nodeKey, _c = _a.numEvents, numEvents = _c === void 0 ? 5 : _c;
    var errors = [];
    events.forEach(function (e) {
        var _a;
        (_a = e === null || e === void 0 ? void 0 : e.errors) === null || _a === void 0 ? void 0 : _a.forEach(function (error) {
            errors.push(__assign(__assign({}, error), { transaction: e.transaction }));
        });
    });
    var type = nodeKey === 'current' ? 'black' : 'white';
    if (errors.length > 0) {
        type = nodeKey === 'current' ? 'error' : 'warning';
        text = (<div>
        <IconFire size="xs"/>
        {text}
      </div>);
    }
    if (events.length === 1 && errors.length === 0) {
        var target = generateSingleEventTarget(events[0], organization, location);
        if (nodeKey === 'current') {
            return (<EventNode pad={pad} type={type}>
          {text}
        </EventNode>);
        }
        else {
            /**
             * When there is only 1 event, clicking the node should take the user directly to
             * the event without additional steps.
             */
            return (<StyledEventNode text={text} pad={pad} hoverText={hoverText} to={target} onClick={function () { return handleNode(nodeKey, organization); }} type={type}/>);
        }
    }
    else {
        /**
         * When there is more than 1 event, clicking the node should expand a dropdown to
         * allow the user to select which event to go to.
         */
        return (<DropdownLink caret={false} title={<StyledEventNode text={text} pad={pad} hoverText={hoverText} type={type}/>} anchorRight>
        {errors.slice(0, numEvents).map(function (error, i) {
            var target = generateSingleEventTarget(error, organization, location);
            return (<DropdownNodeItem key={error.event_id} event={error} onSelect={function () { return handleDropdownItem(target, nodeKey, organization, false); }} first={i === 0} organization={organization} subtext="error" subtextType="error"/>);
        })}
        {nodeKey !== 'current' &&
            events.slice(0, numEvents).map(function (event, i) {
                var target = generateSingleEventTarget(event, organization, location);
                return (<DropdownNodeItem key={event.event_id} event={event} onSelect={function () { return handleDropdownItem(target, nodeKey, organization, false); }} first={i === 0 && errors.length === 0} organization={organization} subtext={getDuration(event['transaction.duration'] / 1000, event['transaction.duration'] < 1000 ? 0 : 2, true)} subtextType="default"/>);
            })}
        {events.length > numEvents && hoverText && extrasTarget && (<DropdownItem onSelect={function () { return handleDropdownItem(extrasTarget, nodeKey, organization, true); }}>
            {hoverText}
          </DropdownItem>)}
      </DropdownLink>);
    }
}
function DropdownNodeItem(_a) {
    var event = _a.event, onSelect = _a.onSelect, first = _a.first, organization = _a.organization, subtext = _a.subtext, subtextType = _a.subtextType;
    return (<DropdownItem onSelect={onSelect} first={first}>
      <DropdownItemSubContainer>
        <Projects orgId={organization.slug} slugs={[event.project_slug]}>
          {function (_a) {
        var projects = _a.projects;
        var project = projects.find(function (p) { return p.slug === event.project_slug; });
        return (<ProjectBadge hideName project={project ? project : { slug: event.project_slug }} avatarSize={16}/>);
    }}
        </Projects>
        <StyledTruncate value={event.transaction} expandDirection="left" maxLength={35} leftTrim trimRegex={/\.|\//g}/>
      </DropdownItemSubContainer>
      <SectionSubtext type={subtextType}>{subtext}</SectionSubtext>
    </DropdownItem>);
}
function StyledEventNode(_a) {
    var text = _a.text, hoverText = _a.hoverText, pad = _a.pad, to = _a.to, onClick = _a.onClick, _b = _a.type, type = _b === void 0 ? 'white' : _b;
    return (<Tooltip position="top" containerDisplayMode="inline-flex" title={hoverText}>
      <EventNode type={type} pad={pad} icon={null} to={to} onClick={onClick}>
        {text}
      </EventNode>
    </Tooltip>);
}
//# sourceMappingURL=quickTrace.jsx.map