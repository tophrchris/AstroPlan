# Capture Studio framing extension

Status: Draft registered extension  
Field: `captureStudioFraming`  
Extension schema version: `1`

The Capture Studio framing extension describes an independently scheduled
pointing or panel associated with an AstroPlan target entry. It preserves a
catalog subject for identity while supplying a potentially different pointing
center, field scale, position angle, filters, and equipment context.

See
[`examples/heart-and-soul-region.astroplan`](../examples/heart-and-soul-region.astroplan)
for an unmodified AstroGuide export.

## Coordinate precedence

The target entry's core `catalogId`, coordinates, and name describe the
astronomical subject. The extension's
`panelCenterRightAscensionHoursJ2000` and
`panelCenterDeclinationDegreesJ2000` describe the scheduled pointing center.

Framing-aware readers must use the panel center for pointing and retain the
core coordinates for subject identity and catalog resolution.

## Frame geometry

`frameWidthDegrees` and `frameHeightDegrees` describe the unscaled equipment
field. `frameScale` is a positive multiplier:

```text
effective width  = frameWidthDegrees  * frameScale
effective height = frameHeightDegrees * frameScale
```

`frameRotationDegrees` follows the convention named by
`frameRotationConvention`. Version 1 uses
`degreesEastOfJ2000North`: degrees east of J2000 celestial north for the frame
height axis.

## Fields

| Field | Type | Description |
| --- | --- | --- |
| `schemaVersion` | integer | Extension schema version; currently `1`. |
| `source` | string | Originating workflow, currently `captureStudioSchedule`. |
| `subjectCatalogId` | string | Parent subject catalog identity. |
| `subjectDisplayName` | string | Parent subject display name. |
| `panelId` | string | Stable panel identity within the originating workflow. |
| `panelTitle` | string | Human-readable panel or capture title. |
| `panelTargetCatalogId` | string or null | Catalog identity associated with the panel. |
| `panelTargetDisplayName` | string or null | Display name associated with the panel. |
| `panelCenterRightAscensionHoursJ2000` | number | Scheduled center RA in decimal J2000 hours. |
| `panelCenterDeclinationDegreesJ2000` | number | Scheduled center declination in J2000 degrees. |
| `frameWidthDegrees` | number | Unscaled equipment-frame width in degrees. |
| `frameHeightDegrees` | number | Unscaled equipment-frame height in degrees. |
| `frameScale` | number | Positive multiplier applied to frame width and height. |
| `frameRotationDegrees` | number | Position angle under the declared convention. |
| `frameRotationConvention` | string | Rotation convention identifier. |
| `frameOffsetXDegrees` | number | Stored horizontal framing offset in degrees. |
| `frameOffsetYDegrees` | number | Stored vertical framing offset in degrees. |
| `telescopeId` | string | Stable telescope or rig identifier. |
| `telescopeName` | string | Human-readable telescope or rig name. |
| `filterIds` | string array | Stable filter identifiers. |
| `filterNames` | string array | Human-readable filter names. |
| `activeRigTelescopeId` | string or null | Active rig telescope identifier when exported. |
| `activeRigFilterId` | string or null | Active filter identifier when exported. |
| `activeRigMountChoice` | string or null | Mount orientation context, such as `eq`. |
| `activeRigPowerSource` | string or null | Power-source context used by planning advice. |
| `previewPresentation` | string or null | Preview/survey presentation identifier. |

Unknown fields inside this object must be ignored when a reader can safely
continue.
