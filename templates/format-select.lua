-- Applies the typographic scale (see templates/resume.latex) to custom-style
-- Divs on the PDF/LaTeX build, and reserves vertical space ahead of every
-- heading so nothing is left stranded at the foot of a page. The docx build
-- gets both behaviours from the named styles in templates/reference.docx
-- instead (sizing, plus keepNext/keepLines), so this filter only acts when
-- FORMAT == "latex".
local SIZE_COMMAND = {
  ResumeName = "\\namesize",
  EntryHeader = "\\entryheadersize",
}

-- LEADING values from templates/resume.latex (\entryheadersize and \bodysize),
-- not font sizes. Update these whenever the scale offset there changes, or the
-- reservations silently stop matching real line heights and headings orphan.
local HEADER_LINE_PT = 13.5
local BULLET_LINE_PT = 10.5
local BULLET_LINES_KEPT = 2
local LIST_TOPSEP_PT = 2
-- \sectionheadsize leading (16.5) + \titlespacing's 6pt after-separation.
local SECTION_HEAD_PT = 16.5 + 6

-- Header lines are separated by markdown hard breaks (see resume.md.j2), so the
-- rendered line count is one more than the number of LineBreaks. Experience and
-- Projects headers are 3 lines; Education and Volunteering are 2. Measuring it
-- rather than hardcoding keeps the reservation right when an entry omits a
-- field (e.g. no dates) and renders shorter.
local function count_lines(para)
  local lines = 1
  for _, inline in ipairs(para.content) do
    if inline.t == "LineBreak" then
      lines = lines + 1
    end
  end
  return lines
end

local function is_entry_header(block)
  return block.t == "Div" and block.attributes["custom-style"] == "EntryHeader"
end

-- Space an entry header needs to start on the current page: its own lines plus
-- the first bullet beneath it, which is allowed 2 lines because most wrap.
local function entry_reservation(div)
  local lines = 0
  for _, block in ipairs(div.content) do
    if block.t == "Para" or block.t == "Plain" then
      lines = math.max(lines, count_lines(block))
    end
  end
  return lines * HEADER_LINE_PT + LIST_TOPSEP_PT + BULLET_LINES_KEPT * BULLET_LINE_PT
end

local function needspace(pt)
  -- Rounded up: leading values are fractional once the scale offset is
  -- non-zero, over-reserving by <1pt is harmless where under-reserving lets a
  -- heading orphan, and Lua's %d rejects non-integers outright.
  return pandoc.RawBlock("latex", string.format("\\needspace{%dpt}", math.ceil(pt)))
end

local function apply_size(div)
  local size_cmd = SIZE_COMMAND[div.attributes["custom-style"]]
  if not size_cmd then
    return
  end
  for _, block in ipairs(div.content) do
    if block.t == "Para" or block.t == "Plain" then
      table.insert(block.content, 1, pandoc.RawInline("latex", "{" .. size_cmd .. " "))
      table.insert(block.content, pandoc.RawInline("latex", "}"))
    end
  end
end

function Pandoc(doc)
  if FORMAT ~= "latex" then
    return doc
  end

  for _, block in ipairs(doc.blocks) do
    if block.t == "Div" then
      apply_size(block)
    end
  end

  local out = pandoc.List()
  for i, block in ipairs(doc.blocks) do
    if block.t == "Header" then
      -- A section heading must reserve room for itself AND for whatever the
      -- next block needs, because the following entry header's own \needspace
      -- introduces a legal breakpoint immediately after the heading -- which is
      -- exactly how a heading ends up alone at a page foot. Sections whose
      -- content is a bare list (Awards, Skills) only need a couple of lines.
      local following = doc.blocks[i + 1]
      local extra = BULLET_LINES_KEPT * BULLET_LINE_PT
      if following ~= nil and is_entry_header(following) then
        extra = entry_reservation(following)
      end
      out:insert(needspace(SECTION_HEAD_PT + extra))
    elseif is_entry_header(block) then
      -- Skip when the heading immediately above already reserved for this
      -- entry; a second identical reservation would only add another
      -- breakpoint between the two.
      local preceding = doc.blocks[i - 1]
      if preceding == nil or preceding.t ~= "Header" then
        out:insert(needspace(entry_reservation(block)))
      end
    end
    out:insert(block)
  end

  doc.blocks = out
  return doc
end
