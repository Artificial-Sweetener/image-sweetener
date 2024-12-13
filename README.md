![window](https://github.com/user-attachments/assets/a28eab72-ac42-4a7a-8933-44fe9af23aa7)

This is a simple program written in Python using Pillow for image manipulation and tkinter for GUI. ChatGPT was used heavily to put it together, using GPT4-o.

There is a build for Windows available in releases. You can run this on any platform that supports Python by cloning this repo. You'll need to make sure you have Pillow and tkinter.

To use:
1. Organize the images you want to watermark/scale into one folder

2. Point Image Sweetener at that folder.

3. Create a watermark. I recommend one with transparency. You want the watermark to also include the padding you want, so leave some negative space around the watermark.
4. Point Image Sweetener at that watermark.

5. You can enable corner watermarks and adjust the transparency. You can have all 4 corners be watermarked if you want, or just one.

6. You can enable a center watermark if you want. This one you can also add rotation to. I would think you'd want to make this a lot more transparent so that it's harder to notice, but you can make it also as opaque as you want.

7. Select which social media sites you plan to post the images to. If you're posting to Instagram, it will automatically put black padding around your image for you to make it fit your chosen aspect ratio, which Instagram requires anyway.

8. Click "Process Images"


Your outputs will be in folders nested within the directory your images were inside. The watermarked images will be in /watermarks/ for example. If you chose to watermark the images, then all the images in the other folder (/facebook/, /instagram/, etc) will be watermarked as well. If you didn't, they'll be the unwatermarked versions. The versions in the social media site folders are all the perfect resolution and format for you to post!


Note: It's best to start with PNG files. Stable Diffusion outputs usually are PNGs to start with anyway.


Known issues:

*Math for adding letterboxes/pillarboxes to pictures for Instagram doesn't work properly on wide images. Only use it on images that are taller than the target aspect ratio

*Codebase is horrific. Believe me when I say all the bad ideas were mine and not ChatGPT's. However, it works and the outputs are quality which is really all that matters to me



To-Do

*Fix Instagram aspect ratio math

*Combine 'social media scalers' into one script

*Add preview for watermarks

*Option to stash multiple watermarks for quick access

If you're interested in what I'm doing or want to support me, consider checking out my website! :]
https://artificialsweetener.ai
