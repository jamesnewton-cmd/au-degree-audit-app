import React, { useMemo, useState } from "react";
import "./App.css";

const BLUE = "#1f4e78";

const SUMMARY_META = {
  studentFile: "Aiden_fixed_for_scheduler.csv",
  businessFallFile: "Dynamic_Export (1).csv",
  laFallFile: "Liberal Arts Fall 2026.csv",
  fallScope: "Only Fall 2026 scheduling is used in V5",
  transcriptCount: 11,
  businessSections: 36,
  approvedLaSections: 74,
  creditRule: "Up to 15 credits; 15 preferred, otherwise 12+",
  scheduleRule:
    "3 options; Option 1 = 3 core/major + 2 LA, Option 2 = 4 core/major + 1 LA, Option 3 = all core/major",
  strictScope: "Only configured V5 strict rules are enforced; see Strict_Prereqs sheet",
};

const SUMMARY_CREDITS = [
  { label: "Option 1 — 3 Core/Major + 2 LA", credits: 15 },
  { label: "Option 2 — 4 Core/Major + 1 LA", credits: 15 },
  { label: "Option 3 — All Core/Major", credits: 15 },
];

const OPTIONS = [
  {
    title: "Option 1 — 3 Core/Major + 2 Liberal Arts",
    mwf: [
      {
        course: "MATH-1250",
        description: "Explorations in Mathematics (23)",
        section: "03",
        classNo: "145092",
        days: "MWF",
        start: "11:00AM",
        end: "11:50AM",
        credits: 3,
        tag: "AU3 - Christian Ways of Knowing (Max 3)",
      },
      {
        course: "BSNS-3420",
        description: "Business Law (23)",
        section: "01",
        classNo: "144982",
        days: "MWF",
        start: "01:00PM",
        end: "01:50PM",
        credits: 3,
        tag: "Business Core / AU6 - Global Ways of Knowing (Max 4)",
      },
      {
        course: "BIBL-2000",
        description: "Intro to the Bible (23)",
        section: "02",
        classNo: "144859",
        days: "MWF",
        start: "03:00PM",
        end: "03:50PM",
        credits: 3,
        tag: "RC6 - Humanistic and Artistic Ways of Knowing (Max 12)",
      },
    ],
    tr: [
      {
        course: "BSNS-3130",
        description: "Sports Marketing (23)",
        section: "01",
        classNo: "145031",
        days: "TR",
        start: "08:00AM",
        end: "09:15AM",
        credits: 3,
        tag: "Major",
      },
      {
        course: "BSNS-1050",
        description: "Business as a Profession (23)",
        section: "02",
        classNo: "145021",
        days: "TR",
        start: "09:30AM",
        end: "10:50AM",
        credits: 3,
        tag: "",
      },
    ],
    why: [
      "Built to land at 15 credit hours with exactly 3 core/major classes and 2 approved Liberal Arts / AU Experience classes.",
      "Uses common default category choices where available: MATH-1250 for RC3 and BIBL-2000 for AU2.",
      "Keeps the mix lighter on numbers by avoiding accounting, economics, and analytics in this option.",
      "Does not schedule locked course(s) with unmet strict prerequisites: ACCT-2020, BSNS-2510, BSNS-4500, BSNS-4800.",
    ],
    totalCredits: 15,
  },
  {
    title: "Option 2 — 4 Core/Major + 1 Liberal Arts",
    mwf: [
      {
        course: "BSNS-3120",
        description: "Global Business (23)",
        section: "01",
        classNo: "144958",
        days: "MWF",
        start: "10:00AM",
        end: "10:50AM",
        credits: 3,
        tag: "Business Core / RC5 - Social and Behavioral Ways of Knowing (Max 12)",
      },
      {
        course: "BSNS-3420",
        description: "Business Law (23)",
        section: "01",
        classNo: "144982",
        days: "MWF",
        start: "01:00PM",
        end: "01:50PM",
        credits: 3,
        tag: "Business Core / AU6 - Global Ways of Knowing (Max 4)",
      },
      {
        course: "BSNS-2310_23",
        description: "Business Analytics (23)",
        section: "01",
        classNo: "144843",
        days: "MWF",
        start: "02:00PM",
        end: "02:50PM",
        credits: 3,
        tag: "RC6 - Humanistic and Artistic Ways of Knowing (Max 12)",
      },
    ],
    tr: [
      {
        course: "BSNS-3130",
        description: "Sports Marketing (23)",
        section: "01",
        classNo: "145031",
        days: "TR",
        start: "08:00AM",
        end: "09:15AM",
        credits: 3,
        tag: "Major",
      },
      {
        course: "RLGN-3010",
        description: "Faith in Context (24)",
        section: "02",
        classNo: "144987",
        days: "TR",
        start: "01:00PM",
        end: "02:15PM",
        credits: 3,
        tag: "",
      },
    ],
    why: [
      "Built to land at 15 credit hours with 4 core/major classes and 1 approved Liberal Arts class.",
      "Uses RLGN-3010 as the preferred AU3 choice while keeping the rest of the schedule in the major/core pipeline.",
      "Balances the week at 3 MWF classes and 2 T/Th classes while limiting the numbers-heavy mix to one analytics course.",
      "Does not schedule locked course(s) with unmet strict prerequisites: ACCT-2020, BSNS-2510, BSNS-4500, BSNS-4800.",
    ],
    totalCredits: 15,
  },
  {
    title: "Option 3 — All Core/Major Classes",
    mwf: [
      {
        course: "ACCT-2010",
        description: "Principles of Accounting I (23)",
        section: "01",
        classNo: "145009",
        days: "MWF",
        start: "08:00AM",
        end: "08:50AM",
        credits: 3,
        tag: "Business Core",
      },
      {
        course: "BSNS-3120",
        description: "Global Business (23)",
        section: "01",
        classNo: "144958",
        days: "MWF",
        start: "10:00AM",
        end: "10:50AM",
        credits: 3,
        tag: "Business Core / RC5 - Social and Behavioral Ways of Knowing (Max 12)",
      },
      {
        course: "BSNS-3420",
        description: "Business Law (23)",
        section: "01",
        classNo: "144982",
        days: "MWF",
        start: "01:00PM",
        end: "01:50PM",
        credits: 3,
        tag: "Business Core / AU6 - Global Ways of Knowing (Max 4)",
      },
    ],
    tr: [
      {
        course: "BSNS-3130",
        description: "Sports Marketing (23)",
        section: "01",
        classNo: "145031",
        days: "TR",
        start: "08:00AM",
        end: "09:15AM",
        credits: 3,
        tag: "Major",
      },
      {
        course: "BSNS-1050",
        description: "Business as a Profession (23)",
        section: "02",
        classNo: "145021",
        days: "TR",
        start: "09:30AM",
        end: "10:50AM",
        credits: 3,
        tag: "",
      },
    ],
    why: [
      "Built to land at 15 credit hours using only core/major classes.",
      "This is the most business-heavy option, but it still avoids stacking economics and analytics together.",
      "Includes BSNS-3130 to move the student in the Sports Management sequence while adding ACCT-2010, BSNS-3120, BSNS-3420, and BSNS-1050.",
      "Does not schedule locked course(s) with unmet strict prerequisites: ACCT-2020, BSNS-2510, BSNS-4500, BSNS-4800.",
    ],
    totalCredits: 15,
  },
];

const TRANSCRIPT_ROWS = [
  ["BSNS-2710", "Principles of Management", "3", "In Progress", "", "3", "", ""],
  ["BSNS-2810", "Principles of Marketing", "3", "Completed", "A", "3", "", ""],
  ["COMM-1000", "Intro to Speech Communication", "3", "In Progress", "", "3", "", ""],
  ["ENGL-1110", "Rhetoric and Composition", "3", "Completed", "B", "3", "", ""],
  ["ENGL-1120", "Rhetoric and Research", "3", "In Progress", "", "3", "", ""],
  ["HIST-2110", "American History I", "3", "Completed", "A-", "3", "", ""],
  ["LART-1050", "First-Year Experience Seminar", "1", "Completed", "CR", "1", "", ""],
  ["PETE-1300", "Intro to Sport/Phys Activ/Rec", "2", "In Progress", "", "2", "", ""],
  ["PETE-2250", "Motor Behavior", "3", "In Progress", "", "3", "", ""],
  ["SPRL-1350", "Phys Act I: Team Sports", "3", "Completed", "B-", "3", "", ""],
  ["SPRL-2450", "Phys Act III: Rec Act/Outdoor", "3", "In Progress", "", "3", "", ""],
];

const STRICT_PREREQS = [
  ["ACCT-2020", "ACCT-2010", "Used for Fall 2026 scheduling only"],
  ["BSNS-2510", "ACCT-2010", "Used for Fall 2026 scheduling only"],
  ["BSNS-4500", "BSNS-2510, BSNS-3120", "Used for Fall 2026 scheduling only"],
  ["BSNS-4910", "BSNS-4500", "Used for Fall 2026 scheduling only"],
  ["BSNS-4360", "BSNS-3130", "Used for Fall 2026 scheduling only"],
  ["BSNS-4560", "BSNS-3130", "Used for Fall 2026 scheduling only"],
  ["COMM-2140", "COMM-2130", "Used for Fall 2026 scheduling only"],
  ["BSNS-4800", "BSNS-3130", "Used for Fall 2026 scheduling only"],
];

const REQUIREMENT_STATUS_ROWS = [
  ["ACCT-2010", "Principles of Accounting I", "Business Core", "3", "Ready for Fall 2026", "Yes", "—"],
  ["ACCT-2020", "Principles of Accounting II", "Business Core", "3", "Hold - strict prerequisite not met", "Yes", "ACCT-2010"],
  ["BSNS-1050", "Business as a Profession", "Business Core", "3", "Ready for Fall 2026", "Yes", "—"],
  ["BSNS-2550", "Business Communications", "Business Core", "3", "Ready for Fall 2026", "Yes", "—"],
  ["BSNS-2310", "Spreadsheet Analytics", "Business Core", "3", "Needed - not in Fall 2026 file", "No", "—"],
  ["BSNS-2450_23", "Principles of Business Analytics", "Business Core", "3", "Ready for Fall 2026", "Yes", "—"],
  ["BSNS-2510", "Principles of Finance", "Business Core", "3", "Hold - strict prerequisite not met", "Yes", "ACCT-2010"],
  ["BSNS-2710", "Principles of Management", "Business Core", "3", "Completed / In Progress", "Yes", "—"],
  ["BSNS-2810", "Principles of Marketing", "Business Core", "3", "Completed / In Progress", "Yes", "—"],
  ["BSNS-3120", "Global Business", "Business Core", "3", "Ready for Fall 2026", "Yes", "—"],
  ["BSNS-3420", "Business Law", "Business Core", "3", "Ready for Fall 2026", "Yes", "—"],
  ["BSNS-4500", "Strategic Management", "Business Core", "3", "Hold - strict prerequisite not met", "No", "BSNS-2510, BSNS-3120"],
  ["BSNS-4800", "Business Internship", "Business Core", "3", "Hold - strict prerequisite not met", "Yes", "BSNS-3130"],
  ["BSNS-4910", "Senior Seminar in Business", "Business Core", "3", "Hold - strict prerequisite not met", "No", "BSNS-4500"],
  ["ECON-2010", "Principles of Macroeconomics", "Business Core", "3", "Ready for Fall 2026", "Yes", "—"],
  ["ECON-2020", "Principles of Microeconomics", "Business Core", "3", "Ready for Fall 2026", "Yes", "—"],
  ["BSNS-3130", "Sports Management", "Major", "3", "Ready for Fall 2026", "Yes", "—"],
  ["COMM-2130", "Writing for the Media", "Major", "3", "Needed - not in Fall 2026 file", "No", "—"],
  ["BSNS-4360", "Sponsorship and Sales", "Major", "3", "Hold - strict prerequisite not met", "No", "BSNS-3130"],
  ["BSNS-4560", "Game Day Experience Management", "Major", "3", "Hold - strict prerequisite not met", "No", "BSNS-3130"],
  ["SPRL-3300", "Management of Sports Facilities and Events", "Major", "3", "Needed - not in Fall 2026 file", "No", "—"],
  ["COMM-2140", "Producing Multimedia Content", "Major", "3", "Hold - strict prerequisite not met", "No", "COMM-2130"],
];

const BUSINESS_SECTIONS = [
  ["145009", "ACCT-2010", "01", "Principles of Accounting I (23)", "MWF", "08:00AM", "08:50AM", "3", "In Person"],
  ["144865", "ACCT-2020", "01", "Principles of Accounting II (23)", "MWF", "01:00PM", "01:50PM", "3", "In Person"],
  ["144860", "ACCT-2010", "01", "Intermediate Accounting I (23)", "MWF", "08:00AM", "08:50AM", "3", "In Person"],
  ["144960", "ACCT-3500", "01", "Accounting Information Systems (23)", "MWF", "11:00AM", "11:50AM", "3", "In Person"],
  ["145039", "BSNS-1050", "01", "Business as a Profession (23)", "R", "09:30AM", "10:50AM", "3", "In Person"],
  ["145039", "BSNS-1050", "02", "Business as a Profession (23)", "T", "09:30AM", "10:50AM", "3", "In Person"],
  ["144843", "BSNS-2310_23", "01", "Business Analytics (23)", "MWF", "02:00PM", "02:50PM", "3", "In Person"],
  ["145069", "BSNS-2450_23", "01", "Data Analysis and Decision Making for Business (2…", "TR", "01:00PM", "02:15PM", "3", "In Person"],
  ["144873", "BSNS-2510", "01", "Principles of Finance (23)", "MWF", "08:00AM", "08:50AM", "3", "In Person"],
  ["145098", "BSNS-2550", "01", "Business Communications (25)", "TR", "08:00AM", "09:15AM", "3", "In Person"],
  ["144876", "BSNS-2710", "01", "Principles of Management (23)", "MWF", "10:00AM", "10:50AM", "3", "In Person"],
  ["144990", "BSNS-2810", "01", "Principles of Marketing (23)", "MWF", "09:00AM", "09:50AM", "3", "In Person"],
  ["144999", "BSNS-3100", "01", "Opportunity Identification and Feasibility (23)", "MWF", "01:00PM", "01:50PM", "3", "In Person"],
  ["144958", "BSNS-3120", "01", "Global Business (23)", "MWF", "10:00AM", "10:50AM", "3", "In Person"],
  ["145031", "BSNS-3130", "01", "Sports Marketing (23)", "TR", "08:00AM", "09:15AM", "3", "In Person"],
  ["145033", "BSNS-3150", "OE", "Financial Planning (23)", "", "", "", "3", "Asynchronous Online"],
];

const RC_AU_ROWS = [
  ["RC1 - Written Communication", "6", "6", "Met / In Progress", "7", "ENGL-1110, ENGL-1120"],
  ["RC2 - Speaking and Listening", "6", "3", "Met / In Progress", "5", "COMM-1000"],
  ["RC3 - Quantitative Reasoning", "8", "0", "Still Needed", "8", "None"],
  ["RC4 - Scientific Ways of Knowing", "8", "0", "Still Needed", "5", "None"],
  ["RC5 - Social and Behavioral Ways of Knowing", "12", "0", "Still Needed", "10", "None"],
  ["RC6 - Humanistic and Artistic Ways of Knowing", "12", "3", "Met / In Progress", "8", "HIST-2110"],
  ["AU1 - Understanding College", "1", "1", "Met / In Progress", "0", "LART-1050"],
  ["AU2 - Biblical Literacy", "3", "0", "Still Needed", "4", "None"],
  ["AU3 - Christian Ways of Knowing", "3", "0", "Still Needed", "4", "None"],
  ["AU4 - Personal Wellness", "3", "0", "Still Needed", "7", "None"],
  ["AU5 - Civil Discourse and Conflict Transformation", "3", "0", "Still Needed", "10", "None"],
  ["AU6 - Global Ways of Knowing", "4", "0", "Still Needed", "8", "None"],
];

function optionCredits(option) {
  return option.mwf.concat(option.tr).reduce((sum, r) => sum + Number(r.credits || 0), 0);
}

function classTable(rows) {
  return (
    <table className="sheet-table">
      <thead>
        <tr>
          <th>Course</th>
          <th>Description</th>
          <th>Section</th>
          <th>Class #</th>
          <th>Days</th>
          <th>Start</th>
          <th>End</th>
          <th>Credits</th>
          <th>Category / LA Tag</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((r, idx) => (
          <tr key={`${r.course}-${idx}`}>
            <td>{r.course}</td>
            <td>{r.description}</td>
            <td>{r.section}</td>
            <td>{r.classNo}</td>
            <td>{r.days}</td>
            <td>{r.start}</td>
            <td>{r.end}</td>
            <td>{r.credits}</td>
            <td>{r.tag}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function SectionTitle({ children }) {
  return <div className="section-title">{children}</div>;
}

function BlockTitle({ children }) {
  return <div className="block-title">{children}</div>;
}

function exportOptionCsv(option) {
  const rows = [
    [option.title],
    [],
    ["MWF Classes"],
    ["Course", "Description", "Section", "Class #", "Days", "Start", "End", "Credits", "Category / LA Tag"],
    ...option.mwf.map((r) => [r.course, r.description, r.section, r.classNo, r.days, r.start, r.end, r.credits, r.tag]),
    [],
    ["T/Th Classes"],
    ["Course", "Description", "Section", "Class #", "Days", "Start", "End", "Credits", "Category / LA Tag"],
    ...option.tr.map((r) => [r.course, r.description, r.section, r.classNo, r.days, r.start, r.end, r.credits, r.tag]),
    [],
    ["Total Credits", optionCredits(option)],
    [],
    ["Why this option was chosen"],
    ...option.why.map((w) => [w]),
  ];
  const csv = rows
    .map((r) => r.map((cell) => `"${String(cell ?? "").replace(/"/g, '""')}"`).join(","))
    .join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${option.title.replace(/\s+/g, "_")}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

export default function App() {
  const [selected, setSelected] = useState(0);
  const current = useMemo(() => OPTIONS[selected], [selected]);

  return (
    <div className="sheet-page">
      <div className="sheet-wrap">
        <div className="header-row">Sports Management V5 — Fall 2026 Only</div>

        <div className="meta-grid">
          <div>Student file</div>
          <div>{SUMMARY_META.studentFile}</div>
          <div>Business fall file</div>
          <div>{SUMMARY_META.businessFallFile}</div>
          <div>Liberal arts fall file</div>
          <div>{SUMMARY_META.laFallFile}</div>
          <div>Fall scope</div>
          <div>{SUMMARY_META.fallScope}</div>
          <div>Completed / current transcript rows counted</div>
          <div>{SUMMARY_META.transcriptCount}</div>
          <div>Open business sections loaded</div>
          <div>{SUMMARY_META.businessSections}</div>
          <div>Approved LA fall sections loaded</div>
          <div>{SUMMARY_META.approvedLaSections}</div>
          <div>Credit rule</div>
          <div>{SUMMARY_META.creditRule}</div>
          <div>Schedule rule</div>
          <div>{SUMMARY_META.scheduleRule}</div>
          <div>Strict prereq scope</div>
          <div>{SUMMARY_META.strictScope}</div>
        </div>

        <SectionTitle>Recommended Fall 2026 Schedule Credits</SectionTitle>
        <table className="sheet-table credits-table">
          <tbody>
            {SUMMARY_CREDITS.map((row) => (
              <tr key={row.label}>
                <td>{row.label}</td>
                <td>{row.credits}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="option-tabs">
          {OPTIONS.map((opt, idx) => (
            <button
              key={opt.title}
              className={idx === selected ? "opt-tab active" : "opt-tab"}
              onClick={() => setSelected(idx)}
              type="button"
            >
              {opt.title}
            </button>
          ))}
          <button className="export-btn" type="button" onClick={() => exportOptionCsv(current)}>
            Export This Option
          </button>
        </div>

        <SectionTitle>{current.title}</SectionTitle>
        <BlockTitle>MWF Classes</BlockTitle>
        {classTable(current.mwf)}

        <BlockTitle>T/Th Classes</BlockTitle>
        {classTable(current.tr)}

        <div className="total-row">
          <span>Total Credits</span>
          <span>{optionCredits(current)}</span>
        </div>

        <BlockTitle>Why this option was chosen</BlockTitle>
        <ul className="why-list">
          {current.why.map((w, idx) => (
            <li key={idx}>{w}</li>
          ))}
        </ul>

        <SectionTitle>Aiden Transcript Used in V5</SectionTitle>
        <table className="sheet-table">
          <thead>
            <tr>
              <th>Course Code</th>
              <th>Course Name</th>
              <th>Credits</th>
              <th>Status</th>
              <th>Letter Grade</th>
              <th>Credits</th>
              <th>Status</th>
              <th>Campus</th>
            </tr>
          </thead>
          <tbody>
            {TRANSCRIPT_ROWS.map((r, idx) => (
              <tr key={idx}>
                {r.map((c, i) => (
                  <td key={i}>{c}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>

        <SectionTitle>Configured V5 Strict Prerequisites</SectionTitle>
        <table className="sheet-table">
          <thead>
            <tr>
              <th>Course</th>
              <th>Requires</th>
              <th>Note</th>
            </tr>
          </thead>
          <tbody>
            {STRICT_PREREQS.map((r, idx) => (
              <tr key={idx}>
                <td>{r[0]}</td>
                <td>{r[1]}</td>
                <td>{r[2]}</td>
              </tr>
            ))}
            <tr>
              <td>Note</td>
              <td colSpan={2} className="note-cell">
                These rules are planner-grade strict rules configured for V5, not a full registrar prerequisite catalog.
              </td>
            </tr>
          </tbody>
        </table>

        <SectionTitle>Requirement Status — Fall 2026</SectionTitle>
        <table className="sheet-table">
          <thead>
            <tr>
              <th>Course</th>
              <th>Requirement</th>
              <th>Category</th>
              <th>Credits</th>
              <th>Status</th>
              <th>Open in Fall</th>
              <th>Strict Prereqs</th>
            </tr>
          </thead>
          <tbody>
            {REQUIREMENT_STATUS_ROWS.map((r, idx) => (
              <tr key={idx}>
                {r.map((c, i) => (
                  <td key={i}>{c}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>

        <SectionTitle>Open Falls School of Business Sections — Fall 2026</SectionTitle>
        <table className="sheet-table">
          <thead>
            <tr>
              <th>Class #</th>
              <th>Course</th>
              <th>Section</th>
              <th>Description</th>
              <th>Days</th>
              <th>Start</th>
              <th>End</th>
              <th>Credits</th>
              <th>Instruction Mode</th>
            </tr>
          </thead>
          <tbody>
            {BUSINESS_SECTIONS.map((r, idx) => (
              <tr key={idx}>
                {r.map((c, i) => (
                  <td key={i}>{c}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>

        <SectionTitle>Raven Core / AU Experience Status for Aiden</SectionTitle>
        <table className="sheet-table">
          <thead>
            <tr>
              <th>Category</th>
              <th>Max Hours</th>
              <th>Walker Hours Counted</th>
              <th>Status</th>
              <th>Approved Fall 2026 Options</th>
              <th>Counted Courses</th>
            </tr>
          </thead>
          <tbody>
            {RC_AU_ROWS.map((r, idx) => (
              <tr key={idx}>
                {r.map((c, i) => (
                  <td key={i}>{c}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
