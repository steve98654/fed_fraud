// Detection tool wireframes: what an agency would receive from its first
// prototype. Wireframes use made-up sample records only. No real provider,
// store or vendor is shown, and no figure here is a finding.

export interface Tool {
  slug: string;
  /** Brief slug of the agency the tool is built for. */
  agency: string;
  ideas: string[];
  title: string;
  short: string;
  summary: string;
  /** Who in the agency would use the screen day to day. */
  users: string;
  /** What the agency gets at the end of the Phase 1 window. */
  delivers: string[];
  /** Public data behind the screen. */
  data: string[];
  /** What internal data would add in Phase 2. */
  phase2: string;
}

export const tools: Tool[] = [
  {
    slug: 'hhs-hospice',
    agency: 'hhs',
    ideas: ['HHS-1', 'HHS-2'],
    title: 'Hospice and home health risk map',
    short: 'HHS hospice risk map',
    summary:
      'Scores every hospice and home health agency in a hot spot against its peers, explains each score, and shows the owner network behind clusters of providers.',
    users: 'CMS Center for Program Integrity analysts and HHS-OIG investigators',
    delivers: [
      'Risk map and ranked provider list for Los Angeles County and Minnesota',
      'Reasons behind every score, each compared with county peers',
      'Owner network view linking providers to LEIE exclusions and revocations',
      'Back-test against providers already suspended or charged',
      'Lead packages for the highest-risk networks',
    ],
    data: [
      'CMS hospice and HHA enrollments and All Owners files',
      'Medicare Post-Acute Care and Hospice by Provider',
      'NPPES registry and monthly deactivations',
      'HHS-OIG LEIE, revoked providers, DOJ case releases',
    ],
    phase2:
      'Medicare claims and PECOS enrollment records turn provider scores into claim-level tests (impossible days, phantom patients, recruitment rings).',
  },
  {
    slug: 'dod-set-asides',
    agency: 'dod',
    ideas: ['DOD-1', 'DOD-2'],
    title: 'Set-aside contractor integrity screen',
    short: 'DoD set-aside screen',
    summary:
      'Ranks small business set-aside vendors by front and pass-through signals, follows subaward dollars to the firms doing the work, and maps shared control among bidders.',
    users: 'DoD Office of Small Business Programs, DCIS agents and contracting officers',
    delivers: [
      'Ranked vendor list over FY2021 to FY2026 set-aside awards, with reasons',
      'Subaward flow view showing where set-aside dollars end up',
      'Collusion network view by market (NAICS and contracting office)',
      'Threshold gaming view for sole-source awards',
      'Lead packages, back-tested against DCIS and DOJ set-aside cases',
    ],
    data: [
      'FPDS and USAspending contract actions and subaward reports',
      'SAM.gov entity registrations and exclusions',
      'SBA certification lists (8(a), HUBZone, WOSB, VetCert)',
      'DCIS and DOJ case releases as labeled examples',
    ],
    phase2:
      'WAWF and PIEE invoices, DCAA audits and losing bids show real pass-through shares and allow invoice-level and bid-level collusion tests.',
  },
  {
    slug: 'snap-retailers',
    agency: 'usda',
    ideas: ['USDA-1', 'USDA-2'],
    title: 'SNAP retailer and meal sponsor risk map',
    short: 'USDA SNAP retailer map',
    summary:
      'Scores each SNAP-authorized store against nearby peers and the history of its address, and checks child meal sponsors for claims beyond what their area can support.',
    users: 'FNS Retailer Operations Division, USDA OIG and state child nutrition agencies',
    delivers: [
      'Retailer risk map for two states, scored against nearby peers',
      'Address history: stores re-authorized where a store was disqualified',
      'Owner reuse after disqualification',
      'Meal sponsor capacity screen for one state that publishes CACFP sites',
      'Lead packages, back-tested against disqualified retailers and Feeding Our Future sites',
    ],
    data: [
      'FNS historical SNAP retailer data (authorization and end dates, type, location)',
      'FNS disqualifications and retailer appeal cases',
      'SNAP participation by county and ACS child population by tract',
      'State CACFP sponsor and site lists',
    ],
    phase2:
      'EBT transactions and retailer redemption data (through FNS and states) move the screen from location and ownership signals to trafficking patterns in sales.',
  },
];

export const toolsFor = (agency: string) => tools.filter((t) => t.agency === agency);
