"use client";
import { useState } from "react";

// Mock Data
const T = [
  { n: "LED street lights, 4,000 units", s: "GeM · Pune Municipal Corp", d: "6 days left", m: 92, v: "Bid", c: "ok", r: [["Turnover ₹50 lakh (MSME relaxed)", "ok", "Met"], ["2 similar orders in 3 years", "ok", "Met"], ["BIS certificate", "ok", "Valid"], ["ISO 9001 certificate", "bad", "Expired"], ["EMD ₹1.2 lakh", "ok", "Exempt"]], w: "You meet 4 of 5 requirements. Renew your ISO 9001 certificate to complete the bid." },
  { n: "Annual maintenance of electrical panels", s: "CPPP · Western Railway", d: "11 days left", m: 81, v: "Bid", c: "ok", r: [["Turnover ₹30 lakh", "ok", "Met"], ["Similar work, 1 order", "ok", "Met"], ["Electrical licence", "ok", "Valid"], ["EMD", "ok", "Exempt"]], w: "You meet every requirement. Add your yearly rate to finish the price sheet." },
  { n: "Solar water heaters, 12 hostels", s: "Maharashtra portal", d: "4 days left", m: 58, v: "Check", c: "warn", r: [["Turnover ₹60 lakh", "bad", "Short by ₹8 lakh"], ["MNRE approved model", "ok", "Valid"], ["EMD ₹80,000", "warn", "Pay online"]], w: "Your turnover is below the limit and the deadline is close. Bid only if you can team up with a partner." },
  { n: "HT transformers, 500 kVA", s: "GeM · MSEDCL", d: "9 days left", m: 34, v: "Skip", c: "bad", r: [["5 years of experience", "bad", "You have 2"], ["Type test report", "bad", "Missing"]], w: "Two key requirements are not met, so this tender is not a good fit." }
];

const V = [
  ["GST registration", "Never expires", "ok", "Valid"],
  ["PAN card", "Never expires", "ok", "Valid"],
  ["Udyam certificate", "Renew by 31 Mar 2027", "ok", "Valid"],
  ["ISO 9001 certificate", "Expired 12 Jan 2026", "bad", "Expired"],
  ["BIS licence", "Expires 20 Nov 2026", "warn", "Expires in 46 days"],
  ["Experience letter, Nagpur", "Issued 2024", "ok", "Valid"]
];

const B = [
  ["LED street lights, 4,000 units", "Draft ready, waiting for your approval", "warn"],
  ["Cable laying, Nashik zone", "Submitted 28 Sep, opens 8 Oct", "ok"],
  ["Office UPS supply, NMDC", "Won, order received", "ok"]
];

export default function Page() {
  const [cur, setCur] = useState("tenders");
  const [sel, setSel] = useState(0);
  const [done, setDone] = useState<Record<number, boolean>>({});
  const [toast, setToast] = useState("");

  const handlePrepareBid = () => {
    setDone(prev => ({ ...prev, [sel]: true }));
    setToast("Bid package started. We will ask you to review it.");
    setTimeout(() => setToast(""), 5000);
  };

  const renderTenders = () => {
    const t = T[sel];
    return (
      <>
        <h1>Good morning</h1>
        <div className="mute">4 new tenders match your business today.</div>
        <div className="stats">
          <div className="stat"><b>4</b>New matches</div>
          <div className="stat"><b>2</b>Worth bidding</div>
          <div className="stat"><b>1</b>Document to renew</div>
        </div>
        <div className="split">
          <div>
            {T.map((x, i) => (
              <button
                key={i}
                className="item"
                aria-pressed={i === sel}
                onClick={() => { setSel(i); setToast(""); }}
              >
                <span>
                  <b>{x.n}</b>
                  <span className="mute">{x.s} · {x.d}</span>
                </span>
                <span className={`pill ${x.c}`}>{x.v} {x.m}%</span>
              </button>
            ))}
          </div>
          <div className="card">
            <h2>{t.n}</h2>
            <div className="mute">{t.s}</div>
            <div className="score">
              <b>{t.m}%</b>
              <span className="mute">match</span>
            </div>
            <div className="bar"><i style={{ width: `${t.m}%` }}></i></div>
            <p>{t.w}</p>
            <ul className="chk">
              {t.r.map((r, idx) => (
                <li key={idx}>
                  <span>{r[0]}</span>
                  <span className={`pill ${r[1]}`}>{r[2]}</span>
                </li>
              ))}
            </ul>
            {t.v === "Skip" ? (
              <button className="btn" disabled>Not a good fit</button>
            ) : (
              <button
                className="btn"
                disabled={done[sel]}
                onClick={handlePrepareBid}
              >
                {done[sel] ? 'Bid package started' : 'Prepare bid'}
              </button>
            )}
            <div className="toast">{toast}</div>
          </div>
        </div>
      </>
    );
  };

  const renderVault = () => (
    <>
      <h1>Document vault</h1>
      <div className="mute">Upload each document once. We remind you before it expires.</div>
      <div className="scroll">
        <table>
          <thead>
            <tr>
              <th>Document</th>
              <th>Validity</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {V.map((v, idx) => (
              <tr key={idx}>
                <td>{v[0]}</td>
                <td className="mute">{v[1]}</td>
                <td><span className={`pill ${v[2]}`}>{v[3]}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p><button className="btn">Upload document</button></p>
    </>
  );

  const renderBids = () => (
    <>
      <h1>My bids</h1>
      <div className="mute">Every bid waits for your approval before it is submitted.</div>
      <div style={{ marginTop: '16px' }}>
        {B.map((b, idx) => (
          <div key={idx} className="item" style={{ cursor: 'default' }}>
            <span>
              <b>{b[0]}</b>
              <span className="mute">{b[1]}</span>
            </span>
            <span className={`pill ${b[2]}`}>
              {b[2] === "warn" ? "Review" : "On track"}
            </span>
          </div>
        ))}
      </div>
    </>
  );

  return (
    <div className="app-container">
      <nav className="sidebar">
        <div className="logo">
          <i></i>Tender Agent
        </div>
        <button aria-current={cur === "tenders"} onClick={() => setCur("tenders")}>Tenders</button>
        <button aria-current={cur === "vault"} onClick={() => setCur("vault")}>Document vault</button>
        <button aria-current={cur === "bids"} onClick={() => setCur("bids")}>My bids</button>
      </nav>
      <main className="main-content">
        {cur === "tenders" && renderTenders()}
        {cur === "vault" && renderVault()}
        {cur === "bids" && renderBids()}
      </main>
    </div>
  );
}
