# pydub-stubs

Pydub version: **0.25.1**

**`pydub-stubs` provides type information for [Pydub].**<br>
Only the public interface is guaranteed to be typed.

[Pydub]: https://github.com/jiaaro/pydub

```
pip install pydub-stubs
```

<br>

## Anticipated Questions

### Q: Why is <code>AudioSegment.<i>effect(...)</i></code> missing?

You need to import it as a function from `pydub.effects`.

### Q: What is `Metadata` and `PartialMetadata`?

These are legacy types that have been replaced by the `channels`,
`frame_rate`, and `sample_rate` keyword arguments.

<br>

## Changelog

### Version 0.25.1.0

* **Added v0.25.0 features**<br>
  This includes `pydub.scipy_effects.eq` and new classmethod parameters.

* **Signatures now use literals where possible**<br>
  Overloaded implementations exist as a fallback.

* **Added missing modules**<br>
  `pydub.silence` and `pydub.utils`

<details>
<summary>Previous versions</summary>

### Version 0.24.1.9

* **Add undocumented parameter of `AudioSegment.from_file`**<br>
  `read_ahead_limit` is absent from the documentation but is a supported
  keyword argument.

### Version 0.24.1.8

* **Export other modules**<br>
  Adds exports for effects, exceptions, generators, playback, and scipy_effects

### Version 0.24.1.7

* **Added `AudioSegment._spawn` (again)**<br>
  This was accidentally removed in an earlier version.

* **Improved `pydub.effects.invert_phase`**<br>
  This is technically less accurate as `(0, 0)` is equivalent to `(0, 1)`.

### Version 0.24.1.6

* **Removed testing symbols from `pydub.audio_segment`**<br>

### Version 0.24.1.5

* **Fixed `AudioSegment.export`**<br>
  First param is named `out_f` and isn't required.

### Version 0.24.1.4

* **Improved signature of `AudioSegment.from_file`**<br>
  The keyword arguments for raw/PCM audio don't require `format` to be set to
  either `raw` or `pcm`.

* **Fixed package exports**<br>
  Exports `AudioSegment` from `__init__.py`.

### Version 0.24.1.3

* **Fixed overloads of `AudioSegment.fade`**<br>
  Exactly two of `start`, `end`, and `duration` must be given.

### Version 0.24.1.2

* **Improved `AudioSegment.fade`**<br>
  Changed to use overloads to prevent invalid method calls.

* **Improved `AudioSegment.from_mono_audiosegments`**<br>
  Use a positional-only parameter to ensure there's at least 1 argument.

### Version 0.24.1.1

* **Fixed `AudioSegment.__init__`**<br>
  Use overloads to model correct parameters.

* **Fixed `AudioSegment._spawn`**<br>
  Parameter `overrides` accepts a partial dictionary.

* **Fixed `pydub.scipy_effects.high_pass_filter`**<br>
  Parameter `order` should be `int`, not `float`.

### Version 0.24.1.0

Released

</details>
