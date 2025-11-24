# Create Wireframe Workflow - Complete Analysis

**Analysis Date:** 2025-11-24  
**Workflow Path:** `workflow-init/.bmad/bmm/workflows/diagrams/create-wireframe`

---

## Executive Summary

The create-wireframe workflow is a **complete and well-structured** workflow for generating Excalidraw wireframes for websites and mobile applications. All required components are present and properly configured.

**Status:** ✅ **READY FOR USE**

**Output Location:** Files are saved to `{project-root}/docs/diagrams/wireframe-{timestamp}.excalidraw`

---

## Workflow Components

### 1. Core Configuration Files

#### workflow.yaml
- **Location:** `workflow-init/.bmad/bmm/workflows/diagrams/create-wireframe/workflow.yaml`
- **Status:** ✅ Complete
- **Key Features:**
  - Standalone workflow (can run independently)
  - Properly references config.yaml for output folder
  - Uses timestamp-based file naming
  - All path references are valid

#### instructions.md
- **Location:** `workflow-init/.bmad/bmm/workflows/diagrams/create-wireframe/instructions.md`
- **Status:** ✅ Complete
- **Structure:** 10 well-defined steps
- **Key Features:**
  - Contextual analysis and requirement gathering
  - Theme selection with 3 preset options + custom
  - Structured wireframe building process
  - JSON validation with error recovery
  - Content validation against checklist

#### checklist.md
- **Location:** `workflow-init/.bmad/bmm/workflows/diagrams/create-wireframe/checklist.md`
- **Status:** ✅ Complete
- **Validation Categories:**
  - Layout Structure
  - UI Elements
  - Fidelity levels
  - Annotations
  - Technical Quality

---

## Referenced Resources

### 2. Shared Diagram Resources

#### excalidraw-templates.yaml
- **Location:** `workflow-init/.bmad/bmm/workflows/diagrams/_shared/excalidraw-templates.yaml`
- **Status:** ✅ Complete
- **Contains Templates For:**
  - Flowcharts (start, process, decision, end)
  - Diagrams (component, database, service, external)
  - **Wireframes** (container, header, button, input, text)
  - Dataflows (process, datastore, external, dataflow)

**Wireframe Template Specifications:**
```yaml
wireframe:
  viewport: { x: 0, y: 0, zoom: 0.8 }
  grid: { size: 20 }
  spacing: { vertical: 40, horizontal: 40 }
  elements:
    container: { type: rectangle, width: 800, height: 600, strokeStyle: solid, strokeWidth: 2 }
    header: { type: rectangle, width: 800, height: 80 }
    button: { type: rectangle, width: 120, height: 40, roundness: 4 }
    input: { type: rectangle, width: 300, height: 40, roundness: 4 }
    text: { type: text, fontSize: 16 }
```

#### excalidraw-library.json
- **Location:** `workflow-init/.bmad/bmm/workflows/diagrams/_shared/excalidraw-library.json`
- **Status:** ✅ Complete
- **Library Items:**
  - start-end-circle (ellipse, blue theme)
  - process-rectangle (rounded rectangle, blue theme)
  - decision-diamond (diamond, orange theme)
  - data-store (rectangle, green theme)
  - external-entity (rectangle, purple theme)

---

### 3. Core Excalidraw Resources

#### excalidraw-helpers.md
- **Location:** `workflow-init/.bmad/core/resources/excalidraw/excalidraw-helpers.md`
- **Status:** ✅ Complete
- **Provides:**
  - Text width calculation formula
  - Element grouping rules (CRITICAL for labels)
  - Grid alignment guidelines (20px snap)
  - Arrow creation (straight and elbow)
  - Theme application rules
  - Validation checklist
  - Optimization guidelines

**Key Formula:**
```
text_width = (text.length × fontSize × 0.6) + 20
```

#### validate-json-instructions.md
- **Location:** `workflow-init/.bmad/core/resources/excalidraw/validate-json-instructions.md`
- **Status:** ✅ Complete
- **Provides:**
  - Node.js validation command
  - Common error patterns and fixes
  - Critical rule: NEVER delete file on validation failure

**Validation Command:**
```bash
node -e "JSON.parse(require('fs').readFileSync('FILE_PATH', 'utf8')); console.log('✓ Valid JSON')"
```

---

### 4. Workflow Execution Engine

#### workflow.xml
- **Location:** `workflow-init/.bmad/core/tasks/workflow.xml`
- **Status:** ✅ Complete
- **Governs:**
  - Workflow initialization and variable resolution
  - Step-by-step execution
  - Template output handling
  - Conditional execution
  - Protocol invocation

---

## Configuration Integration

### config.yaml Settings
- **Location:** `workflow-init/.bmad/bmm/config.yaml`
- **Relevant Settings:**
  - `output_folder: '{project-root}/docs'`
  - `project_name: PHC`
  - `user_skill_level: intermediate`

### Output File Path Resolution
```
default_output_file: "{output_folder}/diagrams/wireframe-{timestamp}.excalidraw"
```

**Resolves to:**
```
/Users/user/Documents/GitHub/brain-storm/docs/diagrams/wireframe-2025-11-24-223000.excalidraw
```

---

## Workflow Execution Flow

### Step-by-Step Process

1. **Step 0: Contextual Analysis**
   - Extract wireframe type, fidelity, screen count, device type, save location
   - Skip to Step 5 if all requirements are clear

2. **Step 1: Identify Wireframe Type** (elicit)
   - Options: Website, Mobile App, Web App, Tablet App, Multi-platform
   - Wait for user selection

3. **Step 2: Gather Requirements** (elicit)
   - Fidelity level: Low/Medium/High
   - Screen count: Single/Few/Multiple/Many
   - Device dimensions or standard
   - Save location

4. **Step 3: Check Theme** (elicit)
   - Check for existing theme.json
   - Ask to use if exists

5. **Step 4: Create Theme** (elicit)
   - Present 3 preset themes + custom option
   - Create theme.json based on selection
   - Confirm with user

6. **Step 5: Plan Wireframe Structure**
   - List all screens and purposes
   - Map navigation flow
   - Identify key UI elements
   - Show planned structure for confirmation

7. **Step 6: Load Resources**
   - Load wireframe templates
   - Load library
   - Load theme.json
   - Load helpers

8. **Step 7: Build Wireframe Elements**
   - Follow helpers for proper element creation
   - Build in order: containers → layout → navigation → content → interactive → labels → flow
   - Apply fidelity guidelines

9. **Step 8: Optimize and Save**
   - Strip unused elements
   - Remove deleted elements
   - Save to output file

10. **Step 9: Validate JSON Syntax**
    - Run Node.js validation
    - Fix errors if validation fails (NEVER delete file)
    - Re-validate until passes

11. **Step 10: Validate Content**
    - Check against checklist.md
    - Verify all quality criteria

---

## Theme Presets

### 1. Classic Wireframe
```json
{
  "background": "#ffffff",
  "container": "#f5f5f5",
  "border": "#9e9e9e",
  "text": "#424242"
}
```

### 2. High Contrast
```json
{
  "background": "#ffffff",
  "container": "#eeeeee",
  "border": "#212121",
  "text": "#000000"
}
```

### 3. Blueprint Style
```json
{
  "background": "#1a237e",
  "container": "#3949ab",
  "border": "#7986cb",
  "text": "#ffffff"
}
```

---

## Fidelity Guidelines

### Low Fidelity
- Basic shapes
- Minimal detail
- Placeholder text (e.g., "Lorem ipsum", "Button")
- No styling or colors beyond theme

### Medium Fidelity
- More defined elements
- Some styling (borders, shadows)
- Representative content
- Basic interactions indicated

### High Fidelity
- Detailed elements
- Realistic sizing and spacing
- Actual content examples
- Full interaction annotations
- Near-production appearance

---

## Technical Requirements

### Element Creation Rules

1. **Unique IDs Required:**
   - `shape-id` for shapes
   - `text-id` for text labels
   - `group-id` for grouping

2. **Shape with Label Structure:**
   ```json
   {
     "id": "shape-id",
     "groupIds": ["group-id"],
     "boundElements": [{"type": "text", "id": "text-id"}]
   }
   ```

3. **Text Element Structure:**
   ```json
   {
     "id": "text-id",
     "containerId": "shape-id",
     "groupIds": ["group-id"],
     "textAlign": "center",
     "verticalAlign": "middle"
   }
   ```

### Grid Alignment
- All coordinates snap to 20px grid
- Formula: `Math.round(value / 20) * 20`
- Minimum spacing: 60px between elements

### Arrow Types

**Straight Arrows:** For forward flow (left-to-right, top-to-bottom)
**Elbow Arrows:** For upward flow, backward flow, complex routing

---

## Validation Checklist

### Layout Structure
- [ ] Screen dimensions appropriate for device type
- [ ] Grid alignment (20px) maintained
- [ ] Consistent spacing between UI elements
- [ ] Proper hierarchy (header, content, footer)

### UI Elements
- [ ] All interactive elements clearly marked
- [ ] Buttons, inputs, and controls properly sized
- [ ] Text labels readable and appropriately sized
- [ ] Navigation elements clearly indicated

### Fidelity
- [ ] Matches requested fidelity level
- [ ] Appropriate level of detail
- [ ] Placeholder content used where needed
- [ ] No unnecessary decoration for low-fidelity

### Annotations
- [ ] Key interactions annotated
- [ ] Flow indicators present if multi-screen
- [ ] Important notes included
- [ ] Element purposes clear

### Technical Quality
- [ ] All elements properly grouped
- [ ] Text elements have containerId
- [ ] Snapped to grid
- [ ] No elements with `isDeleted: true`
- [ ] JSON is valid
- [ ] File saved to correct location

---

## Common Use Cases

### 1. Website Wireframe (Desktop)
- Container: 1440x900 or 1920x1080
- Fidelity: Medium to High
- Screens: Home, About, Contact, Product pages

### 2. Mobile App Wireframe (iOS/Android)
- Container: 375x812 (iPhone) or 360x800 (Android)
- Fidelity: Low to Medium
- Screens: Login, Dashboard, Profile, Settings

### 3. Web App Wireframe (Responsive)
- Multiple containers for breakpoints
- Fidelity: Medium to High
- Screens: Dashboard, Data views, Forms

### 4. Multi-platform Wireframe
- Multiple device types in one file
- Fidelity: Medium
- Shows responsive behavior across devices

---

## Error Handling

### JSON Validation Failures

**Common Errors:**
1. Missing comma after property
2. Missing closing bracket/brace
3. Trailing comma before `]` or `}`
4. Missing quote around string

**Recovery Process:**
1. Read error message for line/position
2. Open file at error location
3. Fix syntax error
4. Save file
5. Re-validate
6. Repeat until validation passes

**Critical Rule:** NEVER delete the file - always fix the error

---

## Dependencies

### Required Files (All Present ✅)
1. `workflow.yaml` - Workflow configuration
2. `instructions.md` - Step-by-step instructions
3. `checklist.md` - Validation checklist
4. `excalidraw-templates.yaml` - Element templates
5. `excalidraw-library.json` - Reusable library items
6. `excalidraw-helpers.md` - Creation guidelines
7. `validate-json-instructions.md` - Validation process
8. `workflow.xml` - Execution engine
9. `config.yaml` - Project configuration

### External Dependencies
- Node.js (for JSON validation)
- File system access (for reading/writing)

---

## Recommendations

### For Users

1. **Start Simple:** Begin with low-fidelity, single-screen wireframes
2. **Use Presets:** Choose from the 3 theme presets before creating custom
3. **Plan First:** Complete Step 5 (planning) thoroughly before building
4. **Validate Often:** Run JSON validation after each major change
5. **Save Incrementally:** Don't build entire multi-screen wireframe in one go

### For Developers

1. **Theme Reuse:** Save successful theme.json files for future projects
2. **Template Extension:** Add custom elements to excalidraw-library.json
3. **Automation:** Consider creating shell scripts for common wireframe types
4. **Version Control:** Track wireframe files in git for iteration history

---

## Conclusion

The create-wireframe workflow is **production-ready** with:

✅ Complete file structure  
✅ All dependencies present  
✅ Clear instructions and validation  
✅ Proper error handling  
✅ Flexible configuration  
✅ Multiple fidelity levels supported  
✅ Theme customization available  

**No issues found. Ready for immediate use.**

---

## Quick Start Command

To execute this workflow:

```bash
# From project root
cline execute workflow-init/.bmad/bmm/workflows/diagrams/create-wireframe/workflow.yaml
```

Or simply tell Cline:
> "Create a wireframe for [describe your app/website]"

The workflow will guide you through the entire process interactively.
