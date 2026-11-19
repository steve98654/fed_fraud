// Agency proposals: the pages we take to agency leaders. Each one follows the
// same seven-section template (src/pages/proposals/[slug].astro). Figures are
// read at build time from the repo (budget and fraud ROM table, ROI model,
// pilot kit, briefs, roadmap); only the words below are written by hand.
//
// Rules, as everywhere on this site: exposure and ROM figures are for sizing,
// never findings; savings and return figures read "Pending" until a screen
// passes validation and an Inspector General or DOJ confirms the results.

export interface LegalRoute {
  /** The authority or agreement. */
  basis: string;
  /** What it covers in this pilot. */
  use: string;
}

export interface Proposal {
  /** Brief slug (docs/agencies/<slug>.md). */
  slug: string;
  /** Row in docs/universe/data/agency_budget_fraud_rom.csv. */
  romAbbr: string;
  /** Agency code in docs/proposals/data/roi_results.csv. */
  roiAgency: string;
  /** Roadmap ideas the pilot runs first. */
  leadIdeas: string[];
  /** Draft status shown on the page. */
  status: string;
  /** Section 1: the ask, one paragraph for the agency leader. */
  ask: string;
  /** What the agency gives: plain list for the "cost" box. */
  cost: string[];
  /** Section 2: the main risks, in one line each. */
  risks: string[];
  /** Section 5: pilot scope. */
  pilot: {
    partner: string;
    screen: string;
    data: string;
    where: string;
    outOfScope: string;
  };
  /** Section 5: legal basis. Not legal advice; counsel must review. */
  legal: LegalRoute[];
  /** Typical time to signed agreements, from the legal track. */
  agreementTime: string;
  /** Section 6: how the ROI model applies to this agency. */
  returnNote: string;
}

const STANDARD_COST = [
  'A sponsor (Assistant IG or equivalent) for 1 hour every two weeks',
  'A data steward for about 2 hours a week',
  'Two investigators for 4 days in total to review 100 leads',
  'Counsel and privacy officer review in days 0 to 10',
  'No new system inside your boundary; about 80 staff hours in all',
];

export const proposals: Proposal[] = [
  {
    slug: 'hhs',
    romAbbr: 'HHS',
    roiAgency: 'HHS',
    leadIdeas: ['HHS-1', 'HHS-2'],
    status: 'Draft v0.1 for discussion. Recommended first pilot partner.',
    ask:
      'We propose a 90-day pilot with HHS-OIG and the CMS Center for Program Integrity on hospice and home health, the sector CMS froze to new Medicare enrollment in May 2026. We would run our provider risk map (HHS-1), already built on public CMS files, against Medicare hospice and home health claims for California and Minnesota inside your environment, and hand your investigators ranked leads with the reasons behind each one. You decide every action. The pilot stops at day 75 if it does not beat a bar we agree in advance.',
    cost: STANDARD_COST,
    risks: [
      'Sham and captive hospices that enroll in clusters, bill heavily within months and change owners when caught',
      'Patients enrolled in hospice who are not terminally ill; long stays and dementia-only diagnoses',
      'Home health, durable medical equipment, lab and telehealth billing by the same owner networks',
      'Medicaid fraud in state-run programs, visible federally only through T-MSIS',
    ],
    pilot: {
      partner: 'HHS-OIG Office of Investigations and Office of Audit Services; CMS Center for Program Integrity',
      screen: 'HHS-1 hospice and home health risk map, plus cluster scoring and exclusion matching (HHS-2)',
      data: 'Medicare hospice and home health claims for California and Minnesota, 2022 to 2026; provider enrollment with owners (PECOS)',
      where: 'Inside the OIG’s or CMS’s authorized environment, or the CMS Virtual Research Data Center',
      outOfScope: 'Beneficiary contact, payment suspension decisions and any adverse action',
    },
    legal: [
      { basis: 'Inspector General Act of 1978, 5 U.S.C. 401-424', use: 'HHS-OIG access to agency records; an IG investigative match is excepted from the computer matching rules' },
      { basis: 'Privacy Act of 1974, 5 U.S.C. 552a', use: 'Claims name beneficiaries: work under a routine use or OIG access, with beneficiary identifiers excluded or hashed' },
      { basis: 'Payment Integrity Information Act of 2019, 31 U.S.C. 3351-3358', use: 'The agency’s duty to find and reduce improper payments, which the pilot serves' },
      { basis: 'Memorandum of understanding and data use agreement (pilot kit templates)', use: 'Data, environment, output review and term' },
    ],
    agreementTime: '3 to 6 months for agency records about individuals through an OIG partnership; the pilot kit plans 10 days from a ready template',
    returnNote:
      'The ROI model covers Medicare fee-for-service and Medicaid, the two programs with the strongest business case of any modeled. The break-even rate is the share of improper dollars, missed by current controls, the tooling must catch to pay for itself; the pilot measures it.',
  },
  {
    slug: 'dod',
    romAbbr: 'DOD',
    roiAgency: 'DOD',
    leadIdeas: ['DOD-1', 'DOD-2'],
    status: 'Draft v0.1 for discussion.',
    ask:
      'We propose a 90-day pilot with DCIS and the DoD Office of Small Business Programs to find fake small businesses and pass-through fronts in set-aside contracts, and collusion among bidders. Our set-aside screen (DOD-1) and bidder network map (DOD-2) run today on public FPDS, USAspending and SAM.gov data, the same data behind the SBA work. With invoice, subcontract payment and losing bid data inside your environment, they would measure real pass-through shares and test bids directly. Your agents get ranked leads with reasons; you decide every action.',
    cost: STANDARD_COST,
    risks: [
      'Fake or ineligible small businesses winning set-aside awards (8(a), HUBZone, WOSB, SDVOSB)',
      'Pass-through fronts that subcontract most of the work to large or ineligible firms',
      'Bid rigging and rotation among firms with shared owners or addresses',
      'Threshold gaming around sole-source limits; travel pay errors (11% to 13% improper)',
    ],
    pilot: {
      partner: 'DCIS and DoD OIG, with the DoD Office of Small Business Programs and the DOJ Procurement Collusion Strike Force',
      screen: 'DOD-1 set-aside contractor integrity screen and DOD-2 bidder collusion networks',
      data: 'Invoices (WAWF and PIEE), subcontract payment data, DCAA audit findings and losing bids, FY2021 to FY2026, for two markets agreed with DCIS',
      where: 'Inside DoD OIG’s or DCIS’s authorized environment',
      outOfScope: 'Contractor contact, suspension and debarment decisions and any adverse action',
    },
    legal: [
      { basis: 'Inspector General Act of 1978, 5 U.S.C. 401-424', use: 'DoD OIG and DCIS access to contracting and payment records' },
      { basis: 'Data use agreement with the program office or OIG', use: 'Contract and invoice records are about businesses, so the Privacy Act mostly does not apply; sole proprietors are treated as personal data' },
      { basis: 'False Claims Act, 31 U.S.C. 3729-3733', use: 'Lead packages are written so DOJ can use them' },
    ],
    agreementTime: '2 to 6 months for agency records about businesses',
    returnNote:
      'The ROI model does not yet have a DoD row: it starts from GAO improper payment estimates, and procurement fraud is mostly invisible to payment sampling. A DoD business case needs contract-fraud inputs that the pilot itself would supply.',
  },
  {
    slug: 'sba',
    romAbbr: 'SBA',
    roiAgency: 'SBA',
    leadIdeas: ['SBA-1'],
    status: 'Draft v0.1 for discussion. Alternate first pilot partner; the work with Rosemary is the proof of method.',
    ask:
      'We propose to extend the screens already proven on SBA’s pandemic programs to the programs SBA runs every year: 7(a) and 504 loans and 8(a) certifications (SBA-1). A 90-day pilot with SBA OIG would score loan applications and lender files, not just funded loans, so that risky applications and lender or agent rings surface before money goes out. The method, the data and the OIG relationship already exist, which makes this the fastest yes of any agency.',
    cost: STANDARD_COST,
    risks: [
      'Pandemic loss now in recovery: Shuttered Venue grants (68.9% improper), PPP forgiveness (19.2%), PPP guaranty purchases (13.3%)',
      'Borrowers sharing identifiers, addresses and officers across loans',
      'Lenders and loan agents behind many bad loans',
      'Ineligible firms in 8(a) and other contracting certifications',
    ],
    pilot: {
      partner: 'SBA OIG; Office of Capital Access; Office of Credit Risk Management',
      screen: 'SBA-1 pandemic signals extended to 7(a) and 504, plus cross-program matching',
      data: '7(a) and 504 application and lender data, 2020 to 2026',
      where: 'SBA OIG’s environment',
      outOfScope: 'Borrower contact and loan decisions',
    },
    legal: [
      { basis: 'Inspector General Act of 1978, 5 U.S.C. 401-424', use: 'SBA OIG access to application and lender files, building on the existing work' },
      { basis: 'Privacy Act of 1974, 5 U.S.C. 552a', use: 'Many borrowers are sole proprietors, so their records are treated as personal data' },
      { basis: 'Ten-year limitation period for PPP and EIDL fraud (2022 law)', use: 'Pandemic leads found now stay prosecutable to 2030-2032' },
    ],
    agreementTime: '3 to 6 months for records about individuals, shorter where the existing OIG agreement can be extended',
    returnNote:
      'The only SBA program in the ROI model is the closed Shuttered Venue grant program, which does not pay back as a stand-alone build. The case for SBA is proof of method and recovery of pandemic losses, and the live loan programs ride on shared screens.',
  },
  {
    slug: 'usda',
    romAbbr: 'USDA',
    roiAgency: 'USDA',
    leadIdeas: ['USDA-1', 'USDA-2'],
    status: 'Draft v0.1 for discussion.',
    ask:
      'We propose a 90-day pilot with the Food and Nutrition Service and USDA OIG on SNAP retailer trafficking and child meal sponsor fraud, the pattern behind Minnesota’s $250M Feeding Our Future case. Our retailer risk map (USDA-1) and sponsor capacity screen (USDA-2) score stores and sponsors from public data today. With retailer redemption and EBT transaction data for two states, the pilot would detect trafficking from sales patterns and hand Retailer Operations ranked stores with reasons. You decide every action.',
    cost: [...STANDARD_COST.slice(0, 4), 'Help from two state SNAP agencies and one state child nutrition agency with data agreements'],
    risks: [
      'SNAP trafficking: stores exchanging benefits for cash; $10.2B improper in SNAP (10.9%)',
      'Stores re-authorized at addresses, or to owners, already disqualified',
      'Child meal sponsors claiming more meals than their area can support (CACFP 10.5% improper)',
      'Farm program payments with high error rates (Emergency Conservation Program 55.5%)',
    ],
    pilot: {
      partner: 'FNS Retailer Operations Division and USDA OIG, with two state SNAP agencies',
      screen: 'USDA-1 SNAP retailer risk map, plus USDA-2 child meal sponsor capacity screen for one state',
      data: 'Retailer redemption data and EBT transactions for two states; CACFP sponsor claims and site attendance for one state',
      where: 'Inside FNS’s or USDA OIG’s authorized environment, or the state agency’s',
      outOfScope: 'Retailer and recipient contact, disqualification decisions and any adverse action',
    },
    legal: [
      { basis: 'Inspector General Act of 1978, 5 U.S.C. 401-424', use: 'USDA OIG access to FNS retailer records' },
      { basis: 'State data sharing agreements', use: 'EBT transactions are held by states; one agreement per state' },
      { basis: 'Privacy Act of 1974, 5 U.S.C. 552a', use: 'Retailer records are about businesses; recipient identifiers in EBT data are excluded or hashed' },
    ],
    agreementTime: '2 to 6 months for FNS retailer records; 3 to 9 months for each state agreement',
    returnNote:
      'The ROI model covers SNAP, which pays back on cautious assumptions. Child nutrition programs are not yet modeled.',
  },
  {
    slug: 'dhs',
    romAbbr: 'DHS',
    roiAgency: 'DHS',
    leadIdeas: ['DHS-1'],
    status: 'Draft v0.1 for discussion.',
    ask:
      'We propose a 90-day pilot with CBP’s Office of Trade and HSI, working with the DOJ-DHS Trade Fraud Task Force, on customs duty evasion through shell importers and false country of origin, a close cousin of SBA shell-entity fraud. Our importer lead list (DHS-1) works today from public trade data. With entry-level ACE data for two product groups, the pilot would measure underpayment importer by importer and hand CBP ranked importers with reasons. You decide every action.',
    cost: STANDARD_COST,
    risks: [
      'Tariff evasion: undervaluation, false country of origin and transshipment',
      'Shell importers that appear after a tariff change and disappear before audit',
      'FEMA disaster aid fraud after major storms (Public Assistance $0.3B improper)',
      'Contract fraud in CBP, ICE and FEMA awards, which run through FPDS like DoD’s',
    ],
    pilot: {
      partner: 'CBP Office of Trade and HSI, with the DOJ-DHS Trade Fraud Task Force',
      screen: 'DHS-1 tariff-evasion importer lead list for two product groups',
      data: 'Entry-level ACE data (declared value, origin, duty paid) for two product groups; EAPA case outcomes for back-testing',
      where: 'Inside CBP’s authorized environment',
      outOfScope: 'Importer contact, liquidation and penalty decisions and any adverse action',
    },
    legal: [
      { basis: 'Inspector General Act of 1978, 5 U.S.C. 401-424', use: 'DHS OIG access, if the pilot runs through the OIG' },
      { basis: 'Data use agreement with CBP Office of Trade', use: 'Entry records are about businesses; counsel to confirm any trade-data confidentiality limits' },
      { basis: 'False Claims Act, 31 U.S.C. 3729-3733', use: 'Customs evasion is pursued under the Act (the $54.4M Ceratizit settlement); lead packages are written for DOJ' },
    ],
    agreementTime: '2 to 6 months for agency records about businesses',
    returnNote:
      'The ROI model has only FEMA Public Assistance for DHS, which does not pay back as a stand-alone build and should ride on shared screens. Customs evasion is not yet modeled; the pilot would supply the inputs.',
  },
];

export const proposalFor = (slug: string) => proposals.find((p) => p.slug === slug);
