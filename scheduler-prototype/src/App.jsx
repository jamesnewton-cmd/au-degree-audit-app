import { useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Upload,
  FileSpreadsheet,
  GraduationCap,
  CalendarDays,
  CheckCircle2,
  AlertCircle,
  Lock,
  Download,
  Sparkles,
} from "lucide-react";

const MAJOR_REQUIREMENTS = [
  { code: "ACCT 2010", title: "Accounting I", credits: 3, track: "Core" },
  {
    code: "ACCT 2020",
    title: "Accounting II",
    credits: 3,
    track: "Core",
    prereqs: ["ACCT 2010"],
  },
  { code: "BSNS 1050", title: "Intro to Business", credits: 3, track: "Core" },
  { code: "BSNS 2450", title: "Spreadsheet Analytics", credits: 3, track: "Core" },
  {
    code: "BSNS 2510",
    title: "Principles of Finance",
    credits: 3,
    track: "Core",
    prereqs: ["ACCT 2010"],
  },
  { code: "BSNS 2710", title: "Principles of Management", credits: 3, track: "Core" },
  {
    code: "BSNS 3120",
    title: "Global Business",
    credits: 3,
    track: "Core",
    rcAuCategory: "AU6",
  },
  { code: "BSNS 3130", title: "Sports Management", credits: 3, track: "Major" },
  { code: "BSNS 3420", title: "Business Law", credits: 3, track: "Core" },
  {
    code: "BSNS 4360",
    title: "Sponsorship",
    credits: 3,
    track: "Major",
    prereqs: ["BSNS 3130"],
  },
  {
    code: "BSNS 4560",
    title: "Business of the Game Day",
    credits: 3,
    track: "Major",
    prereqs: ["BSNS 3130"],
  },
  { code: "COMM 2130", title: "Writing for the Media", credits: 3, track: "Major" },
  {
    code: "COMM 2140",
    title: "Multimedia Content",
    credits: 3,
    track: "Major",
    prereqs: ["COMM 2130"],
  },
  { code: "ECON 2010", title: "Microeconomics", credits: 3, track: "Core", rcAuCategory: "RC5" },
  {
    code: "ECON 2020",
    title: "Macroeconomics",
    credits: 3,
    track: "Core",
    prereqs: ["ECON 2010"],
  },
];

const DEFAULT_RC_AU = [
  { code: "COMM 1000", title: "Fundamentals of Communication", category: "RC2", credits: 3 },
  { code: "MATH 1250", title: "College Algebra", category: "RC3", credits: 3 },
  { code: "EXSC 2140", title: "Wellness Concepts", category: "RC4", credits: 3 },
  { code: "ECON 2010", title: "Microeconomics", category: "RC5", credits: 3 },
  { code: "HIST 2110", title: "American History", category: "RC6", credits: 3 },
  { code: "BIBL 2000", title: "Biblical Literacy", category: "AU2", credits: 3 },
  { code: "RLGN 3010", title: "Christian Faith", category: "AU3", credits: 3 },
  { code: "PEHS 1000", title: "Lifetime Wellness", category: "AU4", credits: 1 },
  { code: "LART 2000", title: "Civil Discourse", category: "AU5", credits: 3 },
  { code: "BSNS 3120", title: "Global Business", category: "AU6", credits: 3 },
];

const CATEGORY_LIMITS = {
  RC2: "3 hrs",
  RC3: "3 hrs",
  RC4: "3-4 hrs",
  RC5: "3 hrs",
  RC6: "3 hrs",
  AU2: "3 hrs",
  AU3: "3 hrs",
  AU4: "1 hr",
  AU5: "3 hrs",
  AU6: "3 hrs",
};

const NUMBERS_HEAVY = new Set([
  "ACCT 2010",
  "ACCT 2020",
  "ECON 2010",
  "ECON 2020",
  "MATH 1250",
  "BSNS 2450",
  "BSNS 2510",
]);

const SAMPLE_TRANSCRIPT = [
  { course: "BSNS 1050", status: "Completed", grade: "B" },
  { course: "COMM 1000", status: "Completed", grade: "A" },
  { course: "MATH 1250", status: "Completed", grade: "C" },
  { course: "ACCT 2010", status: "Completed", grade: "B" },
  { course: "BSNS 2710", status: "Completed", grade: "B" },
];

const SAMPLE_FALL = [
  {
    course: "BSNS 3130",
    title: "Sports Management",
    section: "01",
    classNumber: "145031",
    days: "TR",
    start: "08:00",
    end: "09:15",
    credits: 3,
  },
  {
    course: "BSNS 3120",
    title: "Global Business",
    section: "01",
    classNumber: "144958",
    days: "MWF",
    start: "10:00",
    end: "10:50",
    credits: 3,
  },
  {
    course: "BSNS 3420",
    title: "Business Law",
    section: "01",
    classNumber: "144982",
    days: "MWF",
    start: "13:00",
    end: "13:50",
    credits: 3,
  },
  {
    course: "ECON 2010",
    title: "Microeconomics",
    section: "01",
    classNumber: "144940",
    days: "MWF",
    start: "09:00",
    end: "09:50",
    credits: 3,
  },
  {
    course: "COMM 2130",
    title: "Writing for the Media",
    section: "01",
    classNumber: "145044",
    days: "TR",
    start: "11:00",
    end: "12:15",
    credits: 3,
  },
  {
    course: "HIST 2110",
    title: "American History",
    section: "01",
    classNumber: "200451",
    days: "MWF",
    start: "11:00",
    end: "11:50",
    credits: 3,
  },
  {
    course: "RLGN 3010",
    title: "Christian Faith",
    section: "01",
    classNumber: "200612",
    days: "TR",
    start: "09:30",
    end: "10:45",
    credits: 3,
  },
  {
    course: "BIBL 2000",
    title: "Biblical Literacy",
    section: "01",
    classNumber: "200508",
    days: "TR",
    start: "13:00",
    end: "14:15",
    credits: 3,
  },
  {
    course: "LART 2000",
    title: "Civil Discourse",
    section: "01",
    classNumber: "200701",
    days: "MWF",
    start: "14:00",
    end: "14:50",
    credits: 3,
  },
  {
    course: "PEHS 1000",
    title: "Lifetime Wellness",
    section: "01",
    classNumber: "200801",
    days: "TR",
    start: "14:30",
    end: "15:20",
    credits: 1,
  },
];

function normalizeCourseCode(value = "") {
  return String(value).replace(/_/g, " ").replace(/\s+/g, " ").trim().toUpperCase();
}

function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  if (!lines.length) return [];
  const split = (line) =>
    line.match(/("[^"]*"|[^,]+)/g)?.map((x) => x.replace(/^"|"$/g, "").trim()) || [];
  const headers = split(lines[0]).map((h) => h.toLowerCase());
  return lines.slice(1).map((line) => {
    const values = split(line);
    const row = {};
    headers.forEach((h, i) => {
      row[h] = values[i] ?? "";
    });
    return row;
  });
}

function minutes(t) {
  const [h, m] = String(t || "0:00").split(":").map(Number);
  return (h || 0) * 60 + (m || 0);
}

function normalizeDays(raw = "") {
  const v = String(raw).toUpperCase().replace(/\s+/g, "");
  if (["TR", "TTH", "T/R", "TTHR"].includes(v)) return "TR";
  if (["MWF", "M/W/F", "MONWEDFRI"].includes(v)) return "MWF";
  if (["MW", "M/W"].includes(v)) return "MW";
  return v || "TBA";
}

function sharesDayPattern(a, b) {
  return normalizeDays(a.days) === normalizeDays(b.days);
}

function overlaps(a, b) {
  if (!sharesDayPattern(a, b)) return false;
  return minutes(a.start) < minutes(b.end) && minutes(b.start) < minutes(a.end);
}

function completedSet(transcript) {
  return new Set(
    transcript
      .filter((r) => {
        const status = String(r.status || "").toLowerCase();
        const grade = String(r.grade || "").toUpperCase();
        return status.includes("completed") || status.includes("transfer") || /^[ABCDFP]/.test(grade);
      })
      .map((r) => normalizeCourseCode(r.course || r.code || r.class || ""))
      .filter(Boolean)
  );
}

function buildRequirementStatus(transcript) {
  const done = completedSet(transcript);
  return MAJOR_REQUIREMENTS.map((req) => {
    if (done.has(req.code)) return { ...req, status: "Completed" };
    const prereqsMet = (req.prereqs || []).every((p) => done.has(p));
    return { ...req, status: prereqsMet ? "Ready" : "Locked" };
  });
}

function buildCategoryStatus(transcript) {
  const done = completedSet(transcript);
  return DEFAULT_RC_AU.map((item) => ({
    ...item,
    limit: CATEGORY_LIMITS[item.category],
    status: done.has(item.code) ? "Met" : "Needed",
  }));
}

function getCourseType(courseCode) {
  const req = MAJOR_REQUIREMENTS.find((r) => r.code === courseCode);
  if (req) return req.track;
  if (DEFAULT_RC_AU.some((r) => r.code === courseCode)) return "Liberal Arts";
  return "Other";
}

function scoreSchedule(courses, targetCredits) {
  const credits = courses.reduce((sum, c) => sum + Number(c.credits || 0), 0);
  const mwfCount = courses.filter((c) => normalizeDays(c.days) === "MWF").length;
  const trCount = courses.filter((c) => normalizeDays(c.days) === "TR").length;
  const balanced =
    [2, 3].includes(mwfCount) && [2, 3].includes(trCount)
      ? 8
      : [1, 4].includes(mwfCount) || [1, 4].includes(trCount)
        ? -2
        : 0;
  const heavyPenalty =
    Math.max(
      0,
      courses.filter((c) => NUMBERS_HEAVY.has(c.course)).length - 2,
    ) * 4;
  const majorCoreCount = courses.filter((c) => getCourseType(c.course) !== "Liberal Arts").length;
  const laCount = courses.filter((c) => getCourseType(c.course) === "Liberal Arts").length;
  const creditFit = credits > 15 ? -100 : -Math.abs(targetCredits - credits) * 2;
  return majorCoreCount * 4 + laCount * 2 + balanced + creditFit - heavyPenalty;
}

function makeExplanation(courses, label) {
  const reasons = [];
  const has3130 = courses.some((c) => c.course === "BSNS 3130");
  const laCourses = courses.filter((c) => getCourseType(c.course) === "Liberal Arts");
  const heavyCount = courses.filter((c) => NUMBERS_HEAVY.has(c.course)).length;
  const mwfCount = courses.filter((c) => normalizeDays(c.days) === "MWF").length;
  const trCount = courses.filter((c) => normalizeDays(c.days) === "TR").length;

  if (has3130) reasons.push("Includes BSNS 3130 to keep the sports management sequence moving.");
  if (laCourses.length)
    reasons.push(
      `Includes ${laCourses.length} Liberal Arts course${laCourses.length > 1 ? "s" : ""} to move Raven Core / AU Experience requirements.`,
    );
  if ([2, 3].includes(mwfCount) && [2, 3].includes(trCount))
    reasons.push("Keeps a balanced MWF / TTh split when possible.");
  if (heavyCount <= 2) reasons.push("Avoids an overly numbers-heavy term when possible.");
  if (label === "Option 1") reasons.push("Built as 3 core/major + 2 Liberal Arts when a valid fall schedule exists.");
  if (label === "Option 2") reasons.push("Built as 4 core/major + 1 Liberal Arts when a valid fall schedule exists.");
  if (label === "Option 3") reasons.push("Built as all core/major when a valid fall schedule exists.");
  return reasons;
}

function buildOptions(transcript, fallCourses, creditTarget = 15) {
  const done = completedSet(transcript);
  const reqStatus = buildRequirementStatus(transcript);
  const unmetMajorCore = reqStatus.filter((r) => r.status === "Ready");
  const unmetLA = DEFAULT_RC_AU.filter((r) => !done.has(r.code));

  const normalizedFall = fallCourses
    .map((c) => ({
      ...c,
      course: normalizeCourseCode(c.course),
      days: normalizeDays(c.days),
      credits: Number(c.credits || 0),
    }))
    .filter((c) => c.course && c.days !== "TBA");

  const readyMajorCoreSections = normalizedFall.filter((c) => unmetMajorCore.some((u) => u.code === c.course));
  const readyLASections = normalizedFall.filter((c) => unmetLA.some((u) => u.code === c.course));

  function candidateSort(a, b, preferLA = false) {
    const aHeavy = NUMBERS_HEAVY.has(a.course) ? 1 : 0;
    const bHeavy = NUMBERS_HEAVY.has(b.course) ? 1 : 0;
    if (aHeavy !== bHeavy) return aHeavy - bHeavy;
    if (preferLA) {
      const aIndex = DEFAULT_RC_AU.findIndex((x) => x.code === a.course);
      const bIndex = DEFAULT_RC_AU.findIndex((x) => x.code === b.course);
      if (aIndex !== bIndex) return aIndex - bIndex;
    }
    return minutes(a.start) - minutes(b.start);
  }

  const corePool = [...readyMajorCoreSections].sort((a, b) => candidateSort(a, b, false));
  const laPool = [...readyLASections].sort((a, b) => candidateSort(a, b, true));

  function buildSingleOption(optionName, targetCoreMajor, targetLA) {
    const selected = [];

    const addFromPool = (pool, neededCount, type) => {
      for (const section of pool) {
        const typeCount = selected.filter((s) => {
          if (type === "CoreMajor") {
            return getCourseType(s.course) !== "Liberal Arts";
          }
          return getCourseType(s.course) === type;
        }).length;
        if (typeCount >= neededCount) continue;
        if (selected.some((s) => s.course === section.course)) continue;
        if (selected.some((s) => overlaps(s, section))) continue;
        const heavyCount = selected.filter((s) => NUMBERS_HEAVY.has(s.course)).length;
        if (NUMBERS_HEAVY.has(section.course) && heavyCount >= 2) continue;
        if (selected.reduce((sum, s) => sum + Number(s.credits || 0), 0) + Number(section.credits || 0) > 15)
          continue;
        selected.push({ ...section, type: getCourseType(section.course) });
      }
    };

    addFromPool(corePool, targetCoreMajor, "CoreMajor");
    addFromPool(laPool, targetLA, "Liberal Arts");

    if (optionName === "Option 2" || optionName === "Option 3") {
      addFromPool(corePool, targetCoreMajor, "CoreMajor");
    }
    if (optionName === "Option 1") {
      addFromPool(laPool, targetLA, "Liberal Arts");
    }

    const credits = selected.reduce((sum, c) => sum + Number(c.credits || 0), 0);
    const grouped = {
      MWF: selected
        .filter((c) => normalizeDays(c.days) === "MWF")
        .sort((a, b) => minutes(a.start) - minutes(b.start)),
      TR: selected
        .filter((c) => normalizeDays(c.days) === "TR")
        .sort((a, b) => minutes(a.start) - minutes(b.start)),
      OTHER: selected
        .filter((c) => !["MWF", "TR"].includes(normalizeDays(c.days)))
        .sort((a, b) => minutes(a.start) - minutes(b.start)),
    };

    let notes = "";
    if (optionName === "Option 1") notes = "3 core/major + 2 Liberal Arts when possible.";
    if (optionName === "Option 2") notes = "4 core/major + 1 Liberal Arts when possible.";
    if (optionName === "Option 3") notes = "All core/major when possible.";

    return {
      name: optionName,
      totalCredits: credits,
      grouped,
      courses: selected,
      notes,
      score: scoreSchedule(selected, creditTarget),
      reasons: makeExplanation(selected, optionName),
    };
  }

  return [
    buildSingleOption("Option 1", 3, 2),
    buildSingleOption("Option 2", 4, 1),
    buildSingleOption("Option 3", 5, 0),
  ];
}

function StatCard({ title, value, icon: Icon }) {
  return (
    <Card className="rounded-2xl shadow-sm">
      <CardContent className="p-5 flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-500">{title}</p>
          <p className="text-2xl font-semibold mt-1">{value}</p>
        </div>
        <div className="p-3 rounded-2xl bg-slate-100">
          <Icon className="h-5 w-5" />
        </div>
      </CardContent>
    </Card>
  );
}

function StatusBadge({ value }) {
  if (value === "Completed" || value === "Met") return <Badge className="rounded-full">{value}</Badge>;
  if (value === "Ready" || value === "Needed") return <Badge variant="secondary" className="rounded-full">{value}</Badge>;
  return (
    <Badge variant="destructive" className="rounded-full">
      {value}
    </Badge>
  );
}

function ScheduleTable({ courses }) {
  if (!courses.length) return <div className="text-sm text-slate-500">No classes in this group.</div>;
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200">
      <table className="w-full text-sm">
        <thead className="bg-slate-50 text-left">
          <tr>
            <th className="px-3 py-2">Course</th>
            <th className="px-3 py-2">Section</th>
            <th className="px-3 py-2">Class #</th>
            <th className="px-3 py-2">Days</th>
            <th className="px-3 py-2">Time</th>
            <th className="px-3 py-2">Credits</th>
          </tr>
        </thead>
        <tbody>
          {courses.map((c, i) => (
            <tr key={`${c.course}-${c.section}-${i}`} className="border-t">
              <td className="px-3 py-2">
                <div className="font-medium">{c.course}</div>
                <div className="text-slate-500 text-xs">{c.title}</div>
              </td>
              <td className="px-3 py-2">{c.section}</td>
              <td className="px-3 py-2">{c.classNumber}</td>
              <td className="px-3 py-2">{c.days}</td>
              <td className="px-3 py-2">
                {c.start}-{c.end}
              </td>
              <td className="px-3 py-2">{c.credits}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function StudentSchedulerDashboard() {
  const [major, setMajor] = useState("Sports Management");
  const [creditTarget, setCreditTarget] = useState("15");
  const [studentName, setStudentName] = useState("Walker");
  const [transcriptRows, setTranscriptRows] = useState(SAMPLE_TRANSCRIPT);
  const [fallRows, setFallRows] = useState(SAMPLE_FALL);
  const [built, setBuilt] = useState(false);

  const requirementStatus = useMemo(() => buildRequirementStatus(transcriptRows), [transcriptRows]);
  const categoryStatus = useMemo(() => buildCategoryStatus(transcriptRows), [transcriptRows]);
  const schedules = useMemo(
    () =>
      built
        ? buildOptions(transcriptRows, fallRows, Number(creditTarget))
        : buildOptions(SAMPLE_TRANSCRIPT, SAMPLE_FALL, 15),
    [transcriptRows, fallRows, creditTarget, built],
  );

  const completedMajor = requirementStatus.filter((r) => r.status === "Completed").length;
  const remainingMajor = requirementStatus.filter((r) => r.status !== "Completed").length;
  const rcMet = categoryStatus.filter((r) => r.status === "Met").length;

  async function handleUpload(event, type) {
    const file = event.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    const rows = parseCsv(text);

    if (type === "transcript") {
      const normalized = rows
        .map((r) => ({
          course: normalizeCourseCode(r.course || r["course code"] || r.code || r.class || r.subject || ""),
          status: r.status || r.result || r["course status"] || "Completed",
          grade: r.grade || r["final grade"] || "",
        }))
        .filter((r) => r.course);
      setTranscriptRows(normalized);
    }

    if (type === "fall") {
      const normalized = rows
        .map((r) => ({
          course: normalizeCourseCode(r.course || r["course code"] || r.code || r.subject || ""),
          title: r.title || r.description || r["course title"] || "",
          section: r.section || r.sec || "",
          classNumber: r["class #"] || r["class number"] || r.crn || r["class nbr"] || "",
          days: normalizeDays(r.days || r.meeting || r["meeting pattern"] || ""),
          start: r.start || r["start time"] || "08:00",
          end: r.end || r["end time"] || "09:15",
          credits: Number(r.credits || r.cr || r.hours || 3),
        }))
        .filter((r) => r.course);
      setFallRows(normalized);
    }
  }

  function handleBuild() {
    setBuilt(true);
  }

  function exportOption(option) {
    const rows = [
      [option.name],
      ["Total Credits", option.totalCredits],
      [],
      ["MWF Classes"],
      ["Course", "Title", "Section", "Class #", "Days", "Start", "End", "Credits"],
      ...option.grouped.MWF.map((c) => [c.course, c.title, c.section, c.classNumber, c.days, c.start, c.end, c.credits]),
      [],
      ["T/Th Classes"],
      ["Course", "Title", "Section", "Class #", "Days", "Start", "End", "Credits"],
      ...option.grouped.TR.map((c) => [c.course, c.title, c.section, c.classNumber, c.days, c.start, c.end, c.credits]),
    ];
    const csv = rows
      .map((r) => r.map((cell) => `"${String(cell ?? "").replace(/"/g, '""')}"`).join(","))
      .join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${studentName || "student"}_${option.name.replace(/\s+/g, "_")}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="min-h-screen bg-slate-100 p-6 md:p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="grid gap-6 lg:grid-cols-[1.2fr_.8fr] items-start">
          <div>
            <div className="flex items-center gap-3 mb-3">
              <div className="p-3 rounded-2xl bg-white shadow-sm">
                <GraduationCap className="h-6 w-6" />
              </div>
              <div>
                <h1 className="text-3xl font-semibold tracking-tight">Student Scheduler Dashboard</h1>
                <p className="text-slate-600 mt-1">
                  Upload a transcript and fall schedule file to generate advisor-ready fall schedule options.
                </p>
              </div>
            </div>
          </div>
          <Card className="rounded-3xl shadow-sm">
            <CardHeader>
              <CardTitle>Build Schedule</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label>Student Name</Label>
                <Input value={studentName} onChange={(e) => setStudentName(e.target.value)} className="mt-2 rounded-xl" />
              </div>
              <div>
                <Label>Transcript CSV</Label>
                <div className="mt-2 flex items-center gap-3">
                  <Input type="file" accept=".csv" onChange={(e) => handleUpload(e, "transcript")} className="rounded-xl" />
                  <Upload className="h-4 w-4 text-slate-500" />
                </div>
              </div>
              <div>
                <Label>Fall Classes CSV</Label>
                <div className="mt-2 flex items-center gap-3">
                  <Input type="file" accept=".csv" onChange={(e) => handleUpload(e, "fall")} className="rounded-xl" />
                  <FileSpreadsheet className="h-4 w-4 text-slate-500" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <Label>Major</Label>
                  <Select value={major} onValueChange={setMajor}>
                    <SelectTrigger className="mt-2 rounded-xl">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Sports Management">Sports Management</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Credit Target</Label>
                  <Select value={creditTarget} onValueChange={setCreditTarget}>
                    <SelectTrigger className="mt-2 rounded-xl">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="12">12</SelectItem>
                      <SelectItem value="15">15</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <Button className="w-full rounded-xl gap-2" onClick={handleBuild}>
                <Sparkles className="h-4 w-4" /> Build Schedule
              </Button>
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-4 md:grid-cols-4">
          <StatCard title="Student" value={studentName} icon={GraduationCap} />
          <StatCard title="Completed Major/Core" value={completedMajor} icon={CheckCircle2} />
          <StatCard title="Remaining Major/Core" value={remainingMajor} icon={AlertCircle} />
          <StatCard title="RC / AU Met" value={rcMet} icon={CalendarDays} />
        </div>

        <div className="grid gap-6 lg:grid-cols-[.95fr_1.05fr]">
          <Card className="rounded-3xl shadow-sm">
            <CardHeader>
              <CardTitle>Requirement Status</CardTitle>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="major">
                <TabsList className="mb-4 rounded-xl">
                  <TabsTrigger value="major">Major / Core</TabsTrigger>
                  <TabsTrigger value="la">Raven Core / AU Experience</TabsTrigger>
                </TabsList>
                <TabsContent value="major" className="space-y-3">
                  {requirementStatus.map((req) => (
                    <div key={req.code} className="flex items-start justify-between gap-3 rounded-2xl border p-3">
                      <div>
                        <div className="font-medium">{req.code}</div>
                        <div className="text-sm text-slate-500">{req.title}</div>
                        <div className="text-xs text-slate-400 mt-1">
                          {req.track}
                          {req.prereqs?.length ? ` • prereq: ${req.prereqs.join(", ")}` : ""}
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {req.status === "Locked" ? <Lock className="h-4 w-4 text-slate-400" /> : null}
                        <StatusBadge value={req.status} />
                      </div>
                    </div>
                  ))}
                </TabsContent>
                <TabsContent value="la" className="space-y-3">
                  {categoryStatus.map((req) => (
                    <div key={req.code} className="flex items-start justify-between gap-3 rounded-2xl border p-3">
                      <div>
                        <div className="font-medium">
                          {req.category}: {req.code}
                        </div>
                        <div className="text-sm text-slate-500">{req.title}</div>
                        <div className="text-xs text-slate-400 mt-1">Max hours: {req.limit}</div>
                      </div>
                      <StatusBadge value={req.status} />
                    </div>
                  ))}
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          <Card className="rounded-3xl shadow-sm">
            <CardHeader>
              <CardTitle>Schedule Options</CardTitle>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="0">
                <TabsList className="mb-4 rounded-xl">
                  {schedules.map((opt, i) => (
                    <TabsTrigger key={opt.name} value={String(i)}>
                      {opt.name}
                    </TabsTrigger>
                  ))}
                </TabsList>
                {schedules.map((opt, i) => (
                  <TabsContent key={opt.name} value={String(i)} className="space-y-5">
                    <div className="rounded-2xl bg-slate-50 p-4 border flex items-start justify-between gap-4">
                      <div>
                        <div className="font-medium">{opt.name}</div>
                        <div className="text-sm text-slate-600 mt-1">{opt.notes}</div>
                        <div className="text-sm font-medium mt-3">Total Credits: {opt.totalCredits}</div>
                      </div>
                      <Button variant="outline" className="rounded-xl gap-2" onClick={() => exportOption(opt)}>
                        <Download className="h-4 w-4" /> Export
                      </Button>
                    </div>
                    <div className="space-y-4">
                      <div>
                        <h3 className="font-medium mb-2">MWF Classes</h3>
                        <ScheduleTable courses={opt.grouped.MWF} />
                      </div>
                      <div>
                        <h3 className="font-medium mb-2">T/Th Classes</h3>
                        <ScheduleTable courses={opt.grouped.TR} />
                      </div>
                      {opt.grouped.OTHER.length > 0 && (
                        <div>
                          <h3 className="font-medium mb-2">Other Meeting Patterns</h3>
                          <ScheduleTable courses={opt.grouped.OTHER} />
                        </div>
                      )}
                    </div>
                    <Card className="rounded-2xl border-dashed shadow-none">
                      <CardContent className="p-4 text-sm text-slate-600 space-y-1">
                        {opt.reasons.map((reason, idx) => (
                          <div key={idx}>• {reason}</div>
                        ))}
                      </CardContent>
                    </Card>
                  </TabsContent>
                ))}
              </Tabs>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
