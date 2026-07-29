# Capture Studio framing extension version 1

When a target contains `captureStudioFraming`, keep the target's core
coordinates as its catalog-subject identity and use these extension fields for
the scheduled pointing:

- `panelCenterRightAscensionHoursJ2000`
- `panelCenterDeclinationDegreesJ2000`

Compute effective frame dimensions as:

```text
effective width  = frameWidthDegrees  * frameScale
effective height = frameHeightDegrees * frameScale
```

`frameRotationDegrees` uses the convention in `frameRotationConvention`.
Version 1 expects `degreesEastOfJ2000North`: degrees east of J2000 celestial
north for the frame height axis.

Treat `panelId` as panel identity. Retain parent subject, panel target,
telescope, filter, active-rig, offsets, and preview fields without normalizing
them. Ignore unknown extension fields when safe.
