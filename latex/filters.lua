-- Pandoc filter for the fed_fraud LaTeX build.
-- 1. Splits a "Title: subtitle" heading into title and subtitle.
-- 2. Points links to sibling Markdown files at the compiled PDFs instead.

function Meta(meta)
  if meta.title and not meta.subtitle then
    local t = pandoc.utils.stringify(meta.title)
    local head, tail = t:match("^(.-):%s+(.+)$")
    if head then
      meta.title = pandoc.MetaInlines(pandoc.Str(head))
      meta.subtitle = pandoc.MetaInlines(pandoc.Str(tail:sub(1, 1):upper() .. tail:sub(2)))
    end
  end
  return meta
end

function Link(link)
  if not link.target:match("^%a+:") then
    link.target = link.target:gsub("%.md(#?)", ".pdf%1")
  end
  return link
end

-- Show sibling-file link text as the PDF name too ("hhs.md" becomes "hhs.pdf").
function Str(s)
  local name = s.text:match("^([%w_%-%./]+)%.md$")
  if name then return pandoc.Str(name .. ".pdf") end
end

-- Tables: render as longtable (breaks across pages) in the template's
-- PlanTable style: navy header row, banded body rows, ragged-right cells.
-- Short columns (numbers, scores) take their natural width with the header
-- stacked one word per line; the rest share the remaining width in
-- proportion to the length of their content.
local function cell_latex(cell)
  local tex = pandoc.write(pandoc.Pandoc(cell.contents), "latex")
  return (tex:gsub("%s+$", ""):gsub("\n\n+", "\\par "):gsub("\n", " "))
end

local function longest_word(s)
  local m = 0
  for w in s:gmatch("%S+") do m = math.max(m, #w) end
  return m
end

local SHORT = 10

function Table(tbl)
  local ncols = #tbl.colspecs
  local head = {}
  for _, row in ipairs(tbl.head.rows) do table.insert(head, row) end
  local body = {}
  for _, b in ipairs(tbl.bodies) do
    for _, row in ipairs(b.body) do table.insert(body, row) end
  end

  local short, weights, total, nshort = {}, {}, 0, 0
  for c = 1, ncols do
    local maxlen, word = 0, 0
    for _, row in ipairs(body) do
      local cell = row.cells[c]
      if cell then
        local s = pandoc.utils.stringify(cell.contents)
        maxlen = math.max(maxlen, #s); word = math.max(word, longest_word(s))
      end
    end
    local headword = 0
    for _, row in ipairs(head) do
      local cell = row.cells[c]
      if cell then headword = math.max(headword, longest_word(pandoc.utils.stringify(cell.contents))) end
    end
    short[c] = maxlen <= SHORT and headword <= 14
    if short[c] then
      nshort = nshort + 1
    else
      weights[c] = math.max(math.min(maxlen, 60), word * 2, headword * 2, 8)
      total = total + weights[c]
    end
  end

  local align_of = { AlignRight = "\\raggedleft", AlignCenter = "\\centering" }
  local spec = {}
  for c = 1, ncols do
    local align = align_of[tbl.colspecs[c][1]] or "\\raggedright"
    if short[c] then
      spec[c] = "l"
    else
      -- share of the width left after the short columns, which take about 6.5 percent each
      local free = math.max(1 - 0.065 * nshort, 0.3)
      spec[c] = string.format(">{%s\\arraybackslash}p{\\dimexpr %.3f\\linewidth-2\\tabcolsep}",
        align, free * weights[c] / total)
    end
  end

  local function row_tex(row, header)
    local cells = {}
    for c = 1, ncols do
      local cell = row.cells[c]
      local t = cell and cell_latex(cell) or ""
      if header then
        if short[c] and t:find(" ") then
          t = "\\makecell[tl]{" .. t:gsub(" ", "\\\\") .. "}"
        end
        t = "\\leavevmode\\color{white}\\bfseries " .. t
      end
      cells[c] = t
    end
    return table.concat(cells, " & ") .. " \\\\"
  end

  local out = {}
  local size = ncols >= 7 and "\\footnotesize" or "\\small"
  table.insert(out, "\\begingroup" .. size .. "\\setlength{\\tabcolsep}{4pt}\\renewcommand{\\arraystretch}{1.25}")
  table.insert(out, "\\rowcolors{2}{white}{geolight}")
  table.insert(out, "\\begin{longtable}[l]{@{}" .. table.concat(spec) .. "@{}}")
  for _, row in ipairs(head) do
    table.insert(out, "\\rowcolor{coolblack}" .. row_tex(row, true))
  end
  table.insert(out, "\\endhead")
  for _, row in ipairs(body) do table.insert(out, row_tex(row, false)) end
  table.insert(out, "\\end{longtable}\\endgroup")
  return pandoc.RawBlock("latex", table.concat(out, "\n"))
end
