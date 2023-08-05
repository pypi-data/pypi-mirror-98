# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydub-stubs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydub-stubs',
    'version': '0.25.1.0',
    'description': 'Stub-only package containing type information for pydub',
    'long_description': "# pydub-stubs\n\nPydub version: **0.25.1**\n\n**`pydub-stubs` provides type information for [Pydub].**<br>\nOnly the public interface is guaranteed to be typed.\n\n[Pydub]: https://github.com/jiaaro/pydub\n\n```\npip install pydub-stubs\n```\n\n<br>\n\n## Anticipated Questions\n\n### Q: Why is <code>AudioSegment.<i>effect(...)</i></code> missing?\n\nYou need to import it as a function from `pydub.effects`.\n\n### Q: What is `Metadata` and `PartialMetadata`?\n\nThese are legacy types that have been replaced by the `channels`,\n`frame_rate`, and `sample_rate` keyword arguments.\n\n<br>\n\n## Changelog\n\n### Version 0.25.1.0\n\n* **Added v0.25.0 features**<br>\n  This includes `pydub.scipy_effects.eq` and new classmethod parameters.\n\n* **Signatures now use literals where possible**<br>\n  Overloaded implementations exist as a fallback.\n\n* **Added missing modules**<br>\n  `pydub.silence` and `pydub.utils`\n\n<details>\n<summary>Previous versions</summary>\n\n### Version 0.24.1.9\n\n* **Add undocumented parameter of `AudioSegment.from_file`**<br>\n  `read_ahead_limit` is absent from the documentation but is a supported\n  keyword argument.\n\n### Version 0.24.1.8\n\n* **Export other modules**<br>\n  Adds exports for effects, exceptions, generators, playback, and scipy_effects\n\n### Version 0.24.1.7\n\n* **Added `AudioSegment._spawn` (again)**<br>\n  This was accidentally removed in an earlier version.\n\n* **Improved `pydub.effects.invert_phase`**<br>\n  This is technically less accurate as `(0, 0)` is equivalent to `(0, 1)`.\n\n### Version 0.24.1.6\n\n* **Removed testing symbols from `pydub.audio_segment`**<br>\n\n### Version 0.24.1.5\n\n* **Fixed `AudioSegment.export`**<br>\n  First param is named `out_f` and isn't required.\n\n### Version 0.24.1.4\n\n* **Improved signature of `AudioSegment.from_file`**<br>\n  The keyword arguments for raw/PCM audio don't require `format` to be set to\n  either `raw` or `pcm`.\n\n* **Fixed package exports**<br>\n  Exports `AudioSegment` from `__init__.py`.\n\n### Version 0.24.1.3\n\n* **Fixed overloads of `AudioSegment.fade`**<br>\n  Exactly two of `start`, `end`, and `duration` must be given.\n\n### Version 0.24.1.2\n\n* **Improved `AudioSegment.fade`**<br>\n  Changed to use overloads to prevent invalid method calls.\n\n* **Improved `AudioSegment.from_mono_audiosegments`**<br>\n  Use a positional-only parameter to ensure there's at least 1 argument.\n\n### Version 0.24.1.1\n\n* **Fixed `AudioSegment.__init__`**<br>\n  Use overloads to model correct parameters.\n\n* **Fixed `AudioSegment._spawn`**<br>\n  Parameter `overrides` accepts a partial dictionary.\n\n* **Fixed `pydub.scipy_effects.high_pass_filter`**<br>\n  Parameter `order` should be `int`, not `float`.\n\n### Version 0.24.1.0\n\nReleased\n\n</details>\n",
    'author': 'SeparateRecords',
    'author_email': 'me@rob.ac',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SeparateRecords/pydub-stubs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
