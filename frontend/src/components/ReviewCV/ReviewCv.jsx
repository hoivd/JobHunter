import React from "react";
import { right } from "../../constants/icons";

const fakeData = {
  name: "John Smith",
  address: "123 Broadway, City, State 12345",
  phones: ["(000) 111-1111", "(111) 111-1112"],
  objective:
    "A position in the field of computers with special interests in business applications programming, information processing, and management systems.",
  education: {
    degree: "Bachelor of Science, Interdisciplinary Science",
    school: "Rensselaer Polytechnic Institute, Troy, NY",
    date: "Expected December 1990",
    concentration: "Computer Science",
    minor: "Management",
  },
  skills: {
    languages:
      "COBOL, IFPS, Focus, Megacalc, Pascal, Modula2, C, APL, SNOBOL, FORTRAN, LISP, SPIRES, BASIC, VSPC Autotab, IBM 370 Assembler, Lotus 1-2-3",
    os: "MTS, TSO, Unix",
  },
  experience: [
    {
      title: "Business Applications Programmer",
      employer:
        "Allied-Signal Bendix Friction Materials Division, Financial Planning Department, Latham, NY",
      date: "Fall 1990",
      bullets: [
        'Developed four "user friendly" forecasting systems each of which produces 18 to 139 individual reports.',
        "Developed or improved almost all IFPS programs used for financial reports.",
      ],
    },
    {
      title: "Research Programmer",
      employer: "Psychology Department, Rensselaer Polytechnic Institute",
      date: "Summer 1990",
      bullets: ["Performed computer aided statistical analysis of data."],
    },
    {
      title: "Assistant Manager",
      employer: "Thunder Restaurant, Canton, CT",
      date: "Summers 1988-89",
      bullets: [
        "Recognized need for, developed, and wrote employee training manual.",
        "Performed various duties including cooking, employee training, ordering, and inventory control.",
      ],
    },
  ],
  community: {
    text: 'Organized and directed the 1988 and 1989 Grand Marshall Week "Basketball Marathon." A 24 hour charity event to benefit the Troy Boys Club. Over 250 people participated each year.',
  },
  activities: [
    "Elected House Manager, Rho Phi Sorority",
    "Elected Sports Chairman",
    "Attended Krannet Leadership Conference",
    "Headed delegation to Rho Phi Congress",
    "Junior varsity basketball team",
    "Participant, seven intramural athletic teams",
  ],
};

const Label = ({ children }) => (
  <div className="font-semibold text-xs uppercase tracking-wider text-right pr-4">
    {children}
  </div>
);

const ReviewCv = ({ setIsPreviewCv }) => {
  const d = fakeData;

  return (
    <div className="h-screen bg-gray-50 flex justify-center p-4 relative">
      <div className="h-full overflow-y-auto no-scrollbar w-full max-w-3xl bg-white shadow-sm pt-6 pb-10 px-6 print:shadow-none print:mx-0 print:my-0 text-xs">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-lg font-serif font-semibold tracking-wide">
            {d.name}
          </h1>
          <div className="h-0.5 bg-gray-800 mt-2 mb-3 mx-16" />
          <div className="text-gray-700">
            <div>{d.address}</div>
            <div>{d.phones.join(" or ")}</div>
          </div>
        </div>

        {/* Content grid with scrollable right column */}
        <div className="mt-6 grid grid-cols-12 gap-x-4">
          {/* Left labels */}
          <div className="col-span-3 space-y-4">
            <Label>Objective</Label>
            <Label>Education</Label>
            <Label>Computer Skills</Label>
            <Label>Experience</Label>
            <Label>Community Service</Label>
            <Label>Extra-curricular Activities</Label>
          </div>

          {/* Right content (scrollable) */}
          <div className="col-span-9 space-y-4 text-gray-800 max-h-[70vh]  pr-2">
            {/* Objective */}
            <p>{d.objective}</p>

            {/* Education */}
            <div>
              <div className="italic font-medium">{d.education.degree}</div>
              <div>
                {d.education.school},{" "}
                <span className="italic">{d.education.date}</span>
              </div>
              <div>Concentration: {d.education.concentration}</div>
              <div>Minor: {d.education.minor}</div>
            </div>

            {/* Skills */}
            <div>
              <div className="italic">Languages & Software:</div>
              <div className="pl-1">{d.skills.languages}</div>
              <div className="italic mt-1">Operating Systems:</div>
              <div className="pl-1">{d.skills.os}</div>
            </div>

            {/* Experience */}
            <div>
              {d.experience.map((exp, idx) => (
                <div key={idx} className="mb-3">
                  <div className="flex justify-between">
                    <div className="italic font-medium">{exp.title}</div>
                    <div>{exp.date}</div>
                  </div>
                  <div>{exp.employer}</div>
                  <ul className="list-disc ml-4 mt-1">
                    {exp.bullets.map((b, i) => (
                      <li key={i}>{b}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            {/* Community Service */}
            <div>{d.community.text}</div>

            {/* Activities */}
            <ul className="ml-4 list-disc">
              {d.activities.map((a, i) => (
                <li key={i}>{a}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
      <div
        onClick={() => {
          setIsPreviewCv(false);
        }}
        className="w-8 h-8 rounded-full flex justify-center items-center bg-gray-200 absolute top-5 left-5 hover:cursor-pointer"
      >
        <img src={right} alt="off preview" className="w-6 " />
      </div>
    </div>
  );
};

export default ReviewCv;
