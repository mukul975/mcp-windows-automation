# Adobe Lightroom MCP Automation Commands - Extended Reference

## Complete MCP Command Reference for Adobe Lightroom

### 📸 Photo Navigation & Selection

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `NEXT_PHOTO`                 | Go to Next Photo                   | `Ctrl + →`                                             | Navigates to the next photo in Library or Develop module.               |
| `PREVIOUS_PHOTO`             | Go to Previous Photo               | `Ctrl + ←`                                             | Navigates to the previous photo.                                        |
| `FIRST_PHOTO`                | Go to First Photo                  | `Ctrl + Home`                                          | Jumps to the first photo in the current collection.                     |
| `LAST_PHOTO`                 | Go to Last Photo                   | `Ctrl + End`                                           | Jumps to the last photo in the current collection.                      |
| `SELECT_ALL_PHOTOS`          | Select All Photos                  | `Ctrl + A`                                             | Selects all photos in the current view.                                 |
| `DESELECT_ALL_PHOTOS`        | Deselect All Photos                | `Ctrl + D`                                             | Deselects all currently selected photos.                                |
| `SELECT_FLAGGED_PHOTOS`      | Select Flagged Photos              | `Ctrl + Alt + A`                                       | Selects all flagged photos in the current collection.                   |
| `SELECT_REJECTED_PHOTOS`     | Select Rejected Photos             | `Ctrl + Alt + Delete`                                  | Selects all rejected photos.                                            |

### 🔍 View & Display Controls

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `ZOOM_IN`                    | Zoom in on Image                   | `Ctrl + =` or `Z` toggle zoom                          | Zooms into the photo (toggle or incrementally).                         |
| `ZOOM_OUT`                   | Zoom out of Image                  | `Ctrl + -` or `Z` toggle zoom                          | Zooms out of the image.                                                 |
| `ZOOM_FIT`                   | Zoom to Fit                        | `Ctrl + 0`                                             | Fits the entire image in the view.                                      |
| `ZOOM_FILL`                  | Zoom to Fill                       | `Ctrl + Alt + 0`                                       | Zooms to fill the view with the image.                                  |
| `ZOOM_100_PERCENT`           | Zoom to 100%                       | `Ctrl + Alt + 0`                                       | Shows image at 100% magnification.                                      |
| `TOGGLE_BEFORE_AFTER`        | Toggle Before/After View           | `\`                                                    | Shows original vs edited version for comparison.                        |
| `TOGGLE_FULLSCREEN`          | Toggle Fullscreen Mode             | `F`                                                    | Toggles between windowed and full screen.                               |
| `TOGGLE_LIGHTS_OUT`          | Toggle Lights Out Mode             | `L`                                                    | Cycles through lights out modes (normal, dim, lights out).              |
| `TOGGLE_INFO_OVERLAY`        | Toggle Info Overlay                | `I`                                                    | Cycles through different info overlays on the image.                    |
| `TOGGLE_GRID_OVERLAY`        | Toggle Grid Overlay                | `Ctrl + Alt + O`                                       | Shows/hides grid overlay on the image.                                  |

### 🗂️ Module Navigation

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `SHOW_LIBRARY_VIEW`          | Switch to Library Module           | `Ctrl + Alt + 1`                                       | Opens Library module.                                                   |
| `SHOW_DEVELOP_VIEW`          | Switch to Develop Module           | `Ctrl + Alt + 2`                                       | Opens Develop module for current image.                                 |
| `SHOW_MAP_VIEW`              | Switch to Map Module               | `Ctrl + Alt + 3`                                       | Opens Map module for location data.                                     |
| `SHOW_BOOK_VIEW`             | Switch to Book Module              | `Ctrl + Alt + 4`                                       | Opens Book module for book creation.                                    |
| `SHOW_SLIDESHOW_VIEW`        | Switch to Slideshow Module        | `Ctrl + Alt + 5`                                       | Opens Slideshow module.                                                 |
| `SHOW_PRINT_VIEW`            | Switch to Print Module             | `Ctrl + Alt + 6`                                       | Opens Print module.                                                     |
| `SHOW_WEB_VIEW`              | Switch to Web Module               | `Ctrl + Alt + 7`                                       | Opens Web module for web galleries.                                     |
| `SHOW_GRID_VIEW`             | Switch to Library Grid View        | `G`                                                    | Shows Library module with grid layout.                                  |
| `SHOW_LOUPE_VIEW`            | Switch to Library Loupe View       | `E`                                                    | Shows Library module with single image view.                            |
| `SHOW_COMPARE_VIEW`          | Switch to Compare View             | `C`                                                    | Shows Compare view in Library.                                          |
| `SHOW_SURVEY_VIEW`           | Switch to Survey View              | `N`                                                    | Shows Survey view for comparing multiple images.                        |

### 🎨 Develop Module - Basic Adjustments

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `INCREASE_EXPOSURE`          | Increase Exposure Slider           | `Shift + →` (on selected slider) or simulate dragging  | Adjusts exposure slightly to the right. Requires Develop module active. |
| `DECREASE_EXPOSURE`          | Decrease Exposure Slider           | `Shift + ←` or simulate dragging                       | Adjusts exposure to the left.                                           |
| `INCREASE_HIGHLIGHTS`        | Increase Highlights Slider         | Focus on Highlights slider + `Shift + →`               | Increases highlights recovery.                                           |
| `DECREASE_HIGHLIGHTS`        | Decrease Highlights Slider         | Focus on Highlights slider + `Shift + ←`               | Decreases highlights (more recovery).                                    |
| `INCREASE_SHADOWS`           | Increase Shadows Slider            | Focus on Shadows slider + `Shift + →`                  | Lifts shadows (brighter).                                               |
| `DECREASE_SHADOWS`           | Decrease Shadows Slider            | Focus on Shadows slider + `Shift + ←`                  | Lowers shadows (darker).                                                |
| `INCREASE_WHITES`            | Increase Whites Slider             | Focus on Whites slider + `Shift + →`                   | Increases white point.                                                  |
| `DECREASE_WHITES`            | Decrease Whites Slider             | Focus on Whites slider + `Shift + ←`                   | Decreases white point.                                                  |
| `INCREASE_BLACKS`            | Increase Blacks Slider             | Focus on Blacks slider + `Shift + →`                   | Increases black point (lighter).                                        |
| `DECREASE_BLACKS`            | Decrease Blacks Slider             | Focus on Blacks slider + `Shift + ←`                   | Decreases black point (darker).                                         |
| `INCREASE_CONTRAST`          | Increase Contrast Slider           | Focus on Contrast slider + `Shift + →`                 | Increments contrast in Develop module.                                  |
| `DECREASE_CONTRAST`          | Decrease Contrast Slider           | Focus on Contrast slider + `Shift + ←`                 | Decrements contrast.                                                    |
| `INCREASE_VIBRANCE`          | Increase Vibrance Slider           | Focus on Vibrance slider + `Shift + →`                 | Increases vibrance (smart saturation).                                  |
| `DECREASE_VIBRANCE`          | Decrease Vibrance Slider           | Focus on Vibrance slider + `Shift + ←`                 | Decreases vibrance.                                                     |
| `INCREASE_SATURATION`        | Increase Saturation Slider         | Focus on Saturation slider + `Shift + →`               | Increases overall saturation.                                           |
| `DECREASE_SATURATION`        | Decrease Saturation Slider         | Focus on Saturation slider + `Shift + ←`               | Decreases overall saturation.                                           |

### 🎯 Develop Module - Advanced Adjustments

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `INCREASE_CLARITY`           | Increase Clarity Slider            | Focus on Clarity slider + `Shift + →`                  | Increases local contrast/clarity.                                       |
| `DECREASE_CLARITY`           | Decrease Clarity Slider            | Focus on Clarity slider + `Shift + ←`                  | Decreases clarity (softer look).                                        |
| `INCREASE_DEHAZE`            | Increase Dehaze Slider             | Focus on Dehaze slider + `Shift + →`                   | Increases atmospheric clarity.                                          |
| `DECREASE_DEHAZE`            | Decrease Dehaze Slider             | Focus on Dehaze slider + `Shift + ←`                   | Decreases dehaze (adds haze effect).                                    |
| `INCREASE_TEMP`              | Increase Temperature Slider        | Focus on Temperature slider + `Shift + →`              | Makes image warmer (more yellow).                                       |
| `DECREASE_TEMP`              | Decrease Temperature Slider        | Focus on Temperature slider + `Shift + ←`              | Makes image cooler (more blue).                                         |
| `INCREASE_TINT`              | Increase Tint Slider               | Focus on Tint slider + `Shift + →`                     | Adds magenta tint.                                                      |
| `DECREASE_TINT`              | Decrease Tint Slider               | Focus on Tint slider + `Shift + ←`                     | Adds green tint.                                                        |
| `AUTO_TONE`                  | Auto Tone Adjustment               | `Ctrl + Shift + A`                                     | Applies automatic tone adjustments.                                     |
| `AUTO_WHITE_BALANCE`         | Auto White Balance                 | `Ctrl + Shift + U`                                     | Applies automatic white balance.                                        |

### 🔧 Tools & Corrections

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `CROP_TOOL`                  | Activate Crop Tool                 | `R`                                                    | Activates crop and straighten tool.                                    |
| `SPOT_REMOVAL_TOOL`          | Activate Spot Removal Tool         | `Q`                                                    | Activates spot removal tool for healing/cloning.                       |
| `RED_EYE_TOOL`               | Activate Red Eye Tool              | `E`                                                    | Activates red eye correction tool.                                      |
| `GRADUATED_FILTER_TOOL`      | Activate Graduated Filter Tool     | `M`                                                    | Activates graduated filter for area adjustments.                       |
| `RADIAL_FILTER_TOOL`         | Activate Radial Filter Tool        | `Shift + M`                                            | Activates radial filter for circular adjustments.                      |
| `ADJUSTMENT_BRUSH_TOOL`      | Activate Adjustment Brush Tool     | `K`                                                    | Activates adjustment brush for painting adjustments.                   |
| `LENS_CORRECTION_TOOL`       | Open Lens Corrections Panel        | `Ctrl + Shift + L`                                     | Opens lens corrections panel.                                           |
| `TRANSFORM_TOOL`             | Open Transform Panel               | `Ctrl + Shift + T`                                     | Opens transform panel for perspective corrections.                      |

### 🏷️ Flagging & Rating

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `FLAG_PICK`                  | Flag as Pick                       | `P`                                                    | Flags current photo as a pick (white flag).                            |
| `FLAG_REJECT`                | Flag as Reject                     | `X`                                                    | Flags current photo as reject (black flag).                            |
| `REMOVE_FLAG`                | Remove Flag                        | `U`                                                    | Removes flag from current photo.                                        |
| `RATE_1_STAR`                | Rate 1 Star                        | `1`                                                    | Assigns 1-star rating to current photo.                                |
| `RATE_2_STARS`               | Rate 2 Stars                       | `2`                                                    | Assigns 2-star rating to current photo.                                |
| `RATE_3_STARS`               | Rate 3 Stars                       | `3`                                                    | Assigns 3-star rating to current photo.                                |
| `RATE_4_STARS`               | Rate 4 Stars                       | `4`                                                    | Assigns 4-star rating to current photo.                                |
| `RATE_5_STARS`               | Rate 5 Stars                       | `5`                                                    | Assigns 5-star rating to current photo.                                |
| `INCREASE_RATING`            | Increase Rating                    | `]`                                                    | Increases rating by one star.                                           |
| `DECREASE_RATING`            | Decrease Rating                    | `[`                                                    | Decreases rating by one star.                                           |
| `REMOVE_RATING`              | Remove Rating                      | `0`                                                    | Removes star rating from current photo.                                 |

### 🎨 Color Labels

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `LABEL_RED`                  | Apply Red Color Label              | `6`                                                    | Applies red color label to current photo.                              |
| `LABEL_YELLOW`               | Apply Yellow Color Label           | `7`                                                    | Applies yellow color label to current photo.                           |
| `LABEL_GREEN`                | Apply Green Color Label            | `8`                                                    | Applies green color label to current photo.                            |
| `LABEL_BLUE`                 | Apply Blue Color Label             | `9`                                                    | Applies blue color label to current photo.                             |
| `LABEL_PURPLE`               | Apply Purple Color Label           | `Shift + 6`                                            | Applies purple color label to current photo.                           |
| `REMOVE_LABEL`               | Remove Color Label                 | `Shift + 0`                                            | Removes color label from current photo.                                |

### 🎨 Presets & Styles

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `APPLY_PRESET_1`             | Apply Custom Preset #1             | `Ctrl + Shift + 1`                                     | Applies user-defined preset from Develop module shortcut.               |
| `APPLY_PRESET_2`             | Apply Custom Preset #2             | `Ctrl + Shift + 2`                                     | Applies user-defined preset #2.                                        |
| `APPLY_PRESET_3`             | Apply Custom Preset #3             | `Ctrl + Shift + 3`                                     | Applies user-defined preset #3.                                        |
| `APPLY_PRESET_4`             | Apply Custom Preset #4             | `Ctrl + Shift + 4`                                     | Applies user-defined preset #4.                                        |
| `APPLY_PRESET_5`             | Apply Custom Preset #5             | `Ctrl + Shift + 5`                                     | Applies user-defined preset #5.                                        |
| `RESET_IMAGE`                | Reset All Edits                    | `Ctrl + Shift + R`                                     | Resets current photo to original settings.                              |
| `RESET_CROP`                 | Reset Crop                         | `Ctrl + Alt + R`                                       | Resets crop to original.                                                |
| `PREVIOUS_DEVELOP_SETTING`   | Previous Develop Setting           | `Ctrl + Alt + ←`                                       | Undoes last develop adjustment.                                         |
| `NEXT_DEVELOP_SETTING`       | Next Develop Setting               | `Ctrl + Alt + →`                                       | Redoes develop adjustment.                                              |

### 📋 Copy & Paste Settings

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `COPY_SETTINGS`              | Copy Develop Settings              | `Ctrl + Shift + C`                                     | Copies all current develop settings.                                    |
| `PASTE_SETTINGS`             | Paste Develop Settings             | `Ctrl + Shift + V`                                     | Pastes copied develop settings to current photo.                        |
| `PASTE_SETTINGS_PREVIOUS`    | Paste Settings from Previous       | `Ctrl + Alt + Shift + V`                               | Pastes settings from previous photo.                                    |
| `SYNC_SETTINGS`              | Sync Settings to Selected          | `Ctrl + Shift + S`                                     | Syncs current settings to all selected photos.                         |
| `AUTO_SYNC_TOGGLE`           | Toggle Auto Sync                   | `Ctrl + Alt + A`                                       | Toggles automatic sync mode.                                            |

### 📤 Export & Output

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `EXPORT_IMAGE`               | Export Current Image               | `Ctrl + Shift + E`                                     | Opens export dialog for the current image.                              |
| `EXPORT_WITH_PREVIOUS`       | Export with Previous Settings      | `Ctrl + Alt + Shift + E`                               | Exports with last used export settings.                                |
| `EXPORT_TO_EMAIL`            | Export for Email                   | `Ctrl + Shift + M`                                     | Exports image optimized for email.                                     |
| `EXPORT_TO_HARD_DRIVE`       | Export to Hard Drive               | `Ctrl + Shift + H`                                     | Exports to hard drive with specified settings.                         |
| `EXPORT_TO_CD`               | Export to CD/DVD                   | `Ctrl + Shift + D`                                     | Exports to CD/DVD.                                                      |
| `PRINT_IMAGE`                | Print Current Image                | `Ctrl + P`                                             | Opens print dialog for current image.                                  |
| `PRINT_CONTACT_SHEET`        | Print Contact Sheet                | `Ctrl + Alt + P`                                       | Creates contact sheet for printing.                                    |

### 🗂️ Collections & Keywords

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `NEW_COLLECTION`             | Create New Collection              | `Ctrl + N`                                             | Creates new collection.                                                 |
| `NEW_SMART_COLLECTION`       | Create New Smart Collection        | `Ctrl + Alt + N`                                       | Creates new smart collection.                                           |
| `ADD_TO_COLLECTION`          | Add to Target Collection           | `B`                                                    | Adds current photo to target collection.                               |
| `REMOVE_FROM_COLLECTION`     | Remove from Collection             | `Ctrl + Alt + Shift + B`                               | Removes current photo from collection.                                  |
| `KEYWORD_TAGGING`            | Open Keyword Tagging               | `Ctrl + K`                                             | Opens keyword tagging panel.                                           |
| `KEYWORD_LIST`               | Show Keyword List                  | `Ctrl + Alt + K`                                       | Shows keyword list panel.                                              |
| `KEYWORD_SUGGESTIONS`        | Show Keyword Suggestions           | `Ctrl + Shift + K`                                     | Shows keyword suggestions.                                              |

### 🔍 Search & Filter

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `FILTER_BY_FLAG`             | Filter by Flag                     | `Ctrl + Alt + F`                                       | Opens filter to show only flagged photos.                              |
| `FILTER_BY_RATING`           | Filter by Rating                   | `Ctrl + Alt + R`                                       | Opens filter to show photos by rating.                                 |
| `FILTER_BY_COLOR_LABEL`      | Filter by Color Label              | `Ctrl + Alt + L`                                       | Opens filter to show photos by color label.                            |
| `FILTER_BY_METADATA`         | Filter by Metadata                 | `Ctrl + Alt + M`                                       | Opens metadata filter options.                                         |
| `CLEAR_FILTER`               | Clear All Filters                  | `Ctrl + Alt + Shift + L`                               | Clears all active filters.                                             |
| `FIND_PHOTOS`                | Find Photos                        | `Ctrl + F`                                             | Opens find/search dialog.                                              |
| `FIND_NEXT`                  | Find Next                          | `F3`                                                   | Finds next occurrence in search.                                       |
| `FIND_PREVIOUS`              | Find Previous                      | `Shift + F3`                                           | Finds previous occurrence in search.                                   |

### 🎥 Video & Slideshow

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `PLAY_SLIDESHOW`             | Play Slideshow                     | `Ctrl + Enter`                                         | Starts slideshow with current settings.                                |
| `PLAY_IMPROMPTU_SLIDESHOW`   | Play Impromptu Slideshow           | `Ctrl + Alt + Enter`                                   | Starts impromptu slideshow.                                           |
| `PAUSE_SLIDESHOW`            | Pause Slideshow                    | `Space`                                                | Pauses/resumes slideshow playback.                                    |
| `STOP_SLIDESHOW`             | Stop Slideshow                     | `Escape`                                               | Stops slideshow and returns to normal view.                           |
| `NEXT_SLIDE`                 | Next Slide                         | `→`                                                    | Advances to next slide in slideshow.                                  |
| `PREVIOUS_SLIDE`             | Previous Slide                     | `←`                                                    | Goes to previous slide in slideshow.                                  |

### 🛠️ Panel & Interface Controls

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `TOGGLE_LEFT_PANELS`         | Toggle Left Panels                 | `Tab`                                                  | Shows/hides left side panels.                                          |
| `TOGGLE_RIGHT_PANELS`        | Toggle Right Panels                | `Shift + Tab`                                          | Shows/hides right side panels.                                         |
| `TOGGLE_ALL_PANELS`          | Toggle All Panels                  | `Ctrl + Shift + Tab`                                   | Shows/hides all panels for maximum image view.                         |
| `TOGGLE_TOOLBAR`             | Toggle Toolbar                     | `T`                                                    | Shows/hides toolbar at bottom.                                         |
| `TOGGLE_FILMSTRIP`           | Toggle Filmstrip                   | `F6`                                                   | Shows/hides filmstrip at bottom.                                       |
| `TOGGLE_HEADER`              | Toggle Header                      | `F5`                                                   | Shows/hides header at top.                                            |
| `CYCLE_SCREEN_MODES`         | Cycle Screen Modes                 | `Ctrl + Shift + F`                                     | Cycles through different screen modes.                                 |
| `TOGGLE_MENU_BAR`            | Toggle Menu Bar                    | `Ctrl + Shift + M`                                     | Shows/hides menu bar.                                                  |

### 🔧 Advanced Features

| **MCP Command**              | **Lightroom Action**               | **Windows Shortcut / Automation Command**              | **Description**                                                         |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| `TOGGLE_CLIPPING_WARNINGS`   | Toggle Clipping Warnings           | `J`                                                    | Shows/hides highlight and shadow clipping warnings.                    |
| `TOGGLE_HISTOGRAM`           | Toggle Histogram                   | `Ctrl + 0`                                             | Shows/hides histogram display.                                         |
| `TOGGLE_FOCUS_MASK`          | Toggle Focus Mask                  | `Ctrl + Alt + Shift + M`                               | Shows/hides focus mask overlay.                                        |
| `TOGGLE_RANGE_MASK`          | Toggle Range Mask                  | `Ctrl + Alt + Shift + R`                               | Shows/hides range mask overlay.                                        |
| `CYCLE_PREVIEW_MODES`        | Cycle Preview Modes                | `Ctrl + J`                                             | Cycles through different preview rendering modes.                      |
| `TOGGLE_SOFT_PROOFING`       | Toggle Soft Proofing               | `S`                                                    | Enables/disables soft proofing for print preview.                      |
| `CREATE_VIRTUAL_COPY`        | Create Virtual Copy                | `Ctrl + '`                                             | Creates virtual copy of current photo.                                 |
| `CONVERT_TO_BLACK_WHITE`     | Convert to Black & White           | `V`                                                    | Applies black and white conversion.                                    |
| `TONE_CURVE_TOOL`            | Open Tone Curve                    | `Ctrl + Alt + 1`                                       | Opens tone curve panel for advanced tonal adjustments.                 |
| `HSL_ADJUSTMENTS`            | Open HSL Adjustments               | `Ctrl + Alt + 2`                                       | Opens HSL (Hue, Saturation, Luminance) panel.                         |

## 🎯 Example MCP Integration Commands

```python
# Example natural language commands that could trigger these actions:
"Navigate to the next photo in Lightroom"  # → NEXT_PHOTO
"Increase the exposure of this image"      # → INCREASE_EXPOSURE  
"Apply my wedding preset to this photo"   # → APPLY_PRESET_1
"Export this image for web"               # → EXPORT_IMAGE
"Flag this as a pick"                     # → FLAG_PICK
"Switch to develop module"                # → SHOW_DEVELOP_VIEW
"Toggle before and after view"            # → TOGGLE_BEFORE_AFTER
"Reset all edits on this image"           # → RESET_IMAGE
"Copy settings from this photo"           # → COPY_SETTINGS
"Zoom to fit the entire image"            # → ZOOM_FIT
```

## 🔧 Implementation Notes

1. **Focus Management**: Many slider adjustments require the specific control to have focus first
2. **Module Context**: Some commands only work in specific modules (Library vs Develop)
3. **Selection State**: Batch operations work on currently selected photos
4. **Keyboard Shortcuts**: Most commands use standard Lightroom keyboard shortcuts
5. **Screen Automation**: Some advanced slider controls may require screen coordinate automation
6. **State Detection**: The MCP server should detect current module and adjust commands accordingly

## 🎨 Advanced Use Cases

- **Batch Processing**: Apply consistent edits to multiple photos
- **Workflow Automation**: Create automated editing workflows
- **Preset Management**: Quickly apply and manage custom presets
- **Export Automation**: Set up automated export processes
- **Review Workflow**: Streamline photo review and selection process
- **Color Grading**: Advanced color correction and grading workflows
