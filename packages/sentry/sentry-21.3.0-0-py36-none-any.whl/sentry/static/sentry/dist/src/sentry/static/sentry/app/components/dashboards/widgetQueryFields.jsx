import { __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { IconAdd, IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { explodeField, generateFieldAsString, } from 'app/utils/discover/fields';
import ColumnEditCollection from 'app/views/eventsV2/table/columnEditCollection';
import { QueryField } from 'app/views/eventsV2/table/queryField';
import { FieldValueKind } from 'app/views/eventsV2/table/types';
import Field from 'app/views/settings/components/forms/field';
function WidgetQueryFields(_a) {
    var displayType = _a.displayType, errors = _a.errors, fields = _a.fields, fieldOptions = _a.fieldOptions, onChange = _a.onChange;
    // Handle new fields being added.
    function handleAdd(event) {
        event.preventDefault();
        var newFields = __spread(fields, ['']);
        onChange(newFields);
    }
    function handleRemove(event, fieldIndex) {
        event.preventDefault();
        var newFields = __spread(fields);
        newFields.splice(fieldIndex, 1);
        onChange(newFields);
    }
    function handleChangeField(value, fieldIndex) {
        var newFields = __spread(fields);
        newFields[fieldIndex] = generateFieldAsString(value);
        onChange(newFields);
    }
    function handleColumnChange(columns) {
        var newFields = columns.map(generateFieldAsString);
        onChange(newFields);
    }
    if (displayType === 'table') {
        return (<Field data-test-id="columns" label={t('Columns')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.fields} required>
        <StyledColumnEditCollection columns={fields.map(function (field) { return explodeField({ field: field }); })} onChange={handleColumnChange} fieldOptions={fieldOptions}/>
      </Field>);
    }
    var hideAddYAxisButton = (['world_map', 'big_number'].includes(displayType) && fields.length === 1) ||
        (['line', 'area', 'stacked_area', 'bar'].includes(displayType) &&
            fields.length === 3);
    return (<Field data-test-id="y-axis" label={t('Y-Axis')} inline={false} style={{ padding: "16px 0 24px 0" }} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.fields} required>
      {fields.map(function (field, i) { return (<QueryFieldWrapper key={field + ":" + i}>
          <QueryField fieldValue={explodeField({ field: field })} fieldOptions={fieldOptions} onChange={function (value) { return handleChangeField(value, i); }} filterPrimaryOptions={function (option) {
        return option.value.kind === FieldValueKind.FUNCTION;
    }}/>
          {fields.length > 1 && (<Button size="zero" borderless onClick={function (event) { return handleRemove(event, i); }} icon={<IconDelete />} title={t('Remove this Y-Axis')} label={t('Remove this Y-Axis')}/>)}
        </QueryFieldWrapper>); })}
      {!hideAddYAxisButton && (<div>
          <Button size="small" icon={<IconAdd isCircled/>} onClick={handleAdd}>
            {t('Add Overlay')}
          </Button>
        </div>)}
    </Field>);
}
var StyledColumnEditCollection = styled(ColumnEditCollection)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(1));
export var QueryFieldWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"])), space(1), space(1));
export default WidgetQueryFields;
var templateObject_1, templateObject_2;
//# sourceMappingURL=widgetQueryFields.jsx.map