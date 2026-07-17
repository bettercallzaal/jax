# JAX Duct/Mechanical Prints Index

Catalog of the mechanical engineering drawings in `Z:\Duct Prints` (JAX Bar Harbor campus) — ductwork, piping, and equipment-schedule sheets, organized by building. Companion to [building_maps_index.md](building_maps_index.md) (architectural floor plans). 263 files cataloged across 26 building folders plus 2 top-level files.

## How to use this index

Each entry gives the building/floor/area, the drawing type (M=mechanical general, MH=mechanical HVAC/ductwork, MP=mechanical piping, MD=mechanical demo, FP=fire protection, E/EL/EP=electrical, P=plumbing), and a summary of equipment tags (AHU/RTU/VAV/EF numbers), duct sizes/CFM where legible, and the project date. Use it to find which file likely documents a given AHU, VAV box, room, or duct run before opening the actual PDF.

## Known data-quality issues found while cataloging

- **Filename/sheet-number mismatches** (the physical file name and the drawing's own internal sheet number disagree — verify against the actual PDF before citing a sheet number to someone):
  - B56: `10040-MH-101.pdf` is internally sheet MH-102; `10040-MH-102.pdf` is internally sheet MH-101.
  - B57: `MH-501.pdf` is internally sheet MH-600; `MH-600.pdf` is internally sheet MH-501. Similarly `MP-100.pdf`↔`MP-101.pdf` and `P-100_Level1.pdf`↔`P-101.pdf` appear swapped.
  - B12/Shop Drawings: filenames carry a "20-ARL" (Building 20) prefix but most sheets' title blocks actually read "Building 12" — the shop-drawing set is filed under the wrong building prefix (or vice versa); a few sheets (M1-1 through P3-1) are for an "Animal Production Rooms and Receiving" project that may genuinely be Building 20 content stored in the B12 folder.
  - B29: `13074_MH-100.pdf`, `13074_MH-101.pdf`, `13074_MH-500.pdf` are filed under B29 but their title blocks read "Building 31/32 (Annex 10/11/12)" — not Building 29.
  - B01 D: `MH112 UNIT 4 MECHANICAL DUCTWORK ROOF PLAN.pdf` title block reads "Building 5 Bioinformatics," not Building 01 Unit D.
- **Likely duplicate files** (same content, different filename/format):
  - B50: `10029_MH-101.pdf` = `B50 groud floor.pdf` (byte-identical); `50.Pent_H2.4_ductwork.pdf` = `B50 3rd floor.pdf` (byte-identical, and both are actually the *Penthouse* plan despite one filename saying "3rd floor"); `B50 G floor Overlay.bmp`/`.jpg` are very likely the same source image in two formats.
  - B53: `B53.zip` contains copies of the five other B53 files already cataloged individually — no new content.
  - B55: `TJL Bldg 55 As-builts 0011.pdf` appears to duplicate a sheet from `TJL_B55_COMP SCIENCE_Pricing Set_082214.pdf` rather than containing a distinct as-built survey.
  - B21/Old: several files (MH-100 through MH-103, `B21.1.ViralVectorDuctwork.pdf`) are explicitly superseded/historical versions per the folder name "Old" — current versions live in the B21 root folder.
- **Files that could not be rendered in this pass** (too large for direct read, and this environment lacks a PDF rasterizer/poppler to page through them — re-catalog later with proper tooling, or open manually for anything urgent): `B01 D/CDs.pdf`, `B01 D/Unit4.3rdFloorReno_06.02/combined.pdf`, `B18/Jackson Labs Library Reno Control Submittal Package (1).pdf` (127 pages), `B21/Viral vector plumbing as-builts.pdf` (29.8MB), most of `B30-32` (no extractable text layer at all, e.g. the `91-36_HV1-5` series, `13074_MH-100/101/500`, `15-02...ANNEX 9...pdf`), `B33/B33.pdf` (24 pages, no text layer), `B74/JAX B74 As Built REV1.pdf` (146 pages, ~48.7MB — partial index/bookmarks only), `B50/50-G.tif` and `B50/B50 groud floor.tif` (binary TIFF, no reader available), `B50/B50 G floor Overlay.bmp` (binary BMP, no reader available). The two top-level `.nwd`/BIM-derived files also can't be opened directly (Navisworks format).

---

## Building 01 (Unit A / B / D / E)

### B01 A/62_M10-1 2nd Floor.pdf
- **Area/Floor**: RAF-MNBF (B01) & ABSL-2 (B55) Renovation, 2nd Floor
- **Type**: MH ductwork plan
- **Summary**: Supply/exhaust registers S1-S4, E1-E6, duct 6" round to 32x12, 10"ø fume hood exhaust, fire dampers, iris/blast-gate dampers for PIV racks, 2" PVC gas-scavenging piping. Plenum depth notes M01-M07 (15-3/8" to 16-1/4"). Harriman Associates, Project 13762, sheet M10.1, "RECORD DRAWING," rev 2 dated 11-08-13 (record issued 05-19-15).

### B01 A/62_M10-1 3rd Floor.pdf
- **Area/Floor**: A1 Vivarium Renovation, 3rd Floor
- **Type**: MH ductwork plan
- **Summary**: Supply/exhaust branches S1/S2/E1/E2 feeding PIV rack branches with iris dampers, 6"-8" round up to 22x18 rectangular. Balance targets 55/44, 28/22 CFM and 90-140 CFM at various branches; 2" PVC gas-scavenging to penthouse. Harriman Associates, Project 19339, sheet M10.1, Construction Documents, dated May 24, 2021.

### B01 A/62_M40-1 3rd Floor.pdf
- **Area/Floor**: A1 Vivarium Renovation, 3rd Floor (schedules)
- **Type**: Mechanical schedule sheet
- **Summary**: Registers/Grilles/Diffusers schedule (E1/E2 12x12-14x14, S1/S2 8x8-10x10 Price Industries); Damper schedule (RD-A/B/C/D Ruskin, 880-3135 CFM, 14x14-18x18); Heating Coil schedule (HC-A 1102 CFM/35.7 MBH, HC-B 3135 CFM/101.6 MBH); Humidifier schedule (HUM-A/B, Armstrong). Same project as above, sheet M40.1, dated May 24, 2021.

### B01 B/01b.2_14-56_2014_MH-100.pdf
- **Area/Floor**: Kumar Behavioral Lab, Vivarium Lab 2656A
- **Type**: MH demo + part plan, schedules, details
- **Summary**: VAV-01B-2656A (795 CFM, 8" inlet), RGD schedule S-1/S-2/E-1/E-2, sound attenuator schedule, EAD-2655/2655A flow-station schedule. Allied Engineering, sheet MH-100, dated October 24, 2014.

### B01 B/01b.2_14-56_2014_MH-600.pdf
- **Area/Floor**: Unit 2 — Da Ting Lin Lab Fit-up
- **Type**: Mechanical/plumbing specifications (text only)
- **Summary**: Written specs — insulation, ductwork/accessories, pipe/valves, VAV terminal boxes, exhaust air monitoring/critical dampers, TAB, ATC, sprinklers. Allied Engineering, sheet MH-600, Project 10036, dated 4/30/2010.

### B01 B/01b_12.10036M MH-100.pdf
- **Area/Floor**: Unit 2 — Da Ting Lin Lab Fit-up
- **Type**: MH part plan, schedules, details
- **Summary**: Relocated diffusers/dampers/DP sensors, VAV connections, ductwork 8x6 to 36x12 to existing intake plenum. Exhaust Air Damper w/ Flow Station schedule, RGD schedule, VAV Box schedule. Allied Engineering, sheet MH-100, Project 10036, dated 4/30/2010.

### B01 B/01b_14.10036M MH-600.pdf
- **Area/Floor**: Unit 2 — Kumar Behavioral Lab
- **Type**: Mechanical/plumbing specifications (text only)
- **Summary**: Piping/fittings, terminal VAV boxes, RGDs, ductwork/duct accessories, TAB, ATC, plumbing fixtures/piping, sprinklers. Allied Engineering, sheet MH-600, same firm/format as 01b_12 above.

### B01 B/M601-19203 (002) Mechanical Schedules.pdf
- **Area/Floor**: Unit 2 — Vivarium/Procedure/Surgical/P&I Training/Storage rooms (2600.1/3600.1, 2625, 2660, 2676, 3625, 3650, 3655)
- **Type**: Mechanical schedules
- **Summary**: Humidifier schedule H-1 through H-10 (Penthouse, 150-1080 CFM); Reheat Coil schedule RHC-1 through RHC-10 (Trane); VAV Terminal schedule SAD-1/EAD-1 through -10 (Ruskin); RGD schedule. SMRT Architects, "JAX Bldg 01b Unit 2 Renovations," Project 19003, sheet M601, "AS-BUILTS 09-25-23."

### B01 B/MH104-19203 (002) Penthouse Ductwork Plan.pdf
- **Area/Floor**: Unit 2 — Penthouse
- **Type**: MH penthouse ductwork plan
- **Summary**: Existing ductwork (orange/green highlight) with new SAD-1/EAD-01 through -10, RHC-1 through -10, H-1 through -10, branches 4" round to 36x20. New work limited to damper/humidifier/coil installation. SMRT Architects, Project 19003, sheet MH104, "AS-BUILTS 09-25-23."

### B01 B/MP104-19203 (002).pdf
- **Area/Floor**: Unit 2 — Penthouse
- **Type**: MP piping plan
- **Summary**: LPS/LPR (2") and HWS/HWR (1½"/1") piping to reheat coils/humidifiers, plus DWH-1 domestic water heater. SMRT Architects, Project 19003, sheet MP104, "AS-BUILTS 09-25-23."

### B01 D/CDs.pdf
- **Area/Floor**: Unit D — likely whole-building Construction Documents (unverified)
- **Type**: Construction Documents set — content NOT independently verified (see Known Issues)
- **Summary**: 15.7MB, modified Dec 4 2023. Could not be rendered page-by-page in this environment. Filename implies a full CD package; re-catalog with a proper PDF renderer before relying on this.

### B01 D/Feed From AHU14/MH101.pdf
- **Area/Floor**: Unit 4 Renovation, First Floor
- **Type**: MH ductwork plan
- **Summary**: "First Floor Ductwork Plan," downstream of AHU-14 per folder name. WBRC, Project 2882.38, "AS BUILT 11-28-03." Duct tags present but small text not reliably legible.

### B01 D/Feed From AHU14/MH102.pdf
- **Area/Floor**: Unit 4 Renovation, Second Floor
- **Type**: MH ductwork plan
- **Summary**: Companion to MH101, also downstream of AHU-14. WBRC, Project 2882.38, "AS BUILT 11-28-03."

### B01 D/MH112 UNIT 4 MECHANICAL DUCTWORK ROOF PLAN.pdf
- **Area/Floor**: Title block reads "Building 5 Bioinformatics," Roof — filed under B01 D (see Known Issues)
- **Type**: MH roof ductwork plan
- **Summary**: Rooftop AHU(s) and ductwork/curbs with an AHU airflow/balance schedule on-sheet. Project 2882.63, dated 07.29.11.

### B01 D/Unit4.3rdFloorReno_06.02/M-001.pdf
- **Area/Floor**: Unit 4 – 2nd & 3rd Floor Renovations (legend, not floor-specific)
- **Type**: M legend/schedule sheet
- **Summary**: Ductwork standards, grille/register schedule, mechanical legend/abbreviations. Project 288247, "ISSUED FOR CONSTRUCTION 06.15.07."

### B01 D/Unit4.3rdFloorReno_06.02/M-501.pdf
- **Area/Floor**: Unit 4 renovation (details)
- **Type**: M details sheet
- **Summary**: Rooftop AHU-2 detail, duct/grille detail, wall/floor fire-damper detail. Project 288247, 06.15.07.

### B01 D/Unit4.3rdFloorReno_06.02/M-502.pdf
- **Area/Floor**: Unit 4 renovation (piping details)
- **Type**: Mechanical piping schematics/details
- **Summary**: Condensate drain trap, fin-tube convector piping, split-system piping schematic. Project 288247.

### B01 D/Unit4.3rdFloorReno_06.02/M-601.pdf
- **Area/Floor**: Unit 4 renovation (schedules)
- **Type**: Mechanical equipment schedules
- **Summary**: Exhaust fan, VAV terminal box, and AHU schedules (CFM/static pressure/HP columns present, row values not legible). Project 288247.

### B01 D/Unit4.3rdFloorReno_06.02/MD104.pdf
- **Area/Floor**: Unit 4 renovation, Roof
- **Type**: MD demolition plan
- **Summary**: Existing rooftop ductwork/equipment marked for removal ahead of 2nd/3rd floor reno. Project 288247.

### B01 D/Unit4.3rdFloorReno_06.02/MH102.pdf
- **Area/Floor**: Unit 4 renovation, 2nd Floor
- **Type**: MH ductwork plan
- **Summary**: Office layout (video conference, telecom, graphics, mailing offices) with supply/return/exhaust duct routing, diffuser tags SD-2/SG-2. Project 288247.

### B01 D/Unit4.3rdFloorReno_06.02/MH102ab.pdf
- **Area/Floor**: Unit 4 renovation, 2nd Floor
- **Type**: MH ductwork plan — alternate/split version of MH102
- **Summary**: Same 2nd-floor office area as MH102 with detail callouts A4/A11; likely an a/b split or working alternate of the same sheet.

### B01 D/Unit4.3rdFloorReno_06.02/MH103.pdf
- **Area/Floor**: Unit 4 renovation, 3rd Floor
- **Type**: MH ductwork plan
- **Summary**: Third-floor room layout, supply/exhaust ductwork and diffuser locations. Project 288247.

### B01 D/Unit4.3rdFloorReno_06.02/MH104.pdf
- **Area/Floor**: Unit 4 renovation, Roof
- **Type**: MH roof ductwork plan
- **Summary**: Rooftop ductwork routing/curbs, companion to MD104 roof demo. Project 288247.

### B01 D/Unit4.3rdFloorReno_06.02/MP102.PDF
- **Area/Floor**: Unit 4 renovation, 2nd Floor
- **Type**: MP piping plan
- **Summary**: Piping routing for 2nd floor reno area (hydronic/convector). Project 288247.

### B01 D/Unit4.3rdFloorReno_06.02/MP103.PDF
- **Area/Floor**: Unit 4 renovation, 3rd Floor
- **Type**: MP piping plan
- **Summary**: Piping routing for 3rd floor, companion to MH103. Project 288247, "ISSUED FOR CONSTRUCTION 06.15.07."

### B01 D/Unit4.3rdFloorReno_06.02/MP104.PDF
- **Area/Floor**: Unit 4 renovation, Roof
- **Type**: MP roof piping plan
- **Summary**: Rooftop piping (condensate/refrigerant/hydronic), companion to MH104. Project 288247.

### B01 D/Unit4.3rdFloorReno_06.02/combined.pdf
- **Area/Floor**: Unit 4 – 2nd & 3rd Floor Renovations (all sheets) — content NOT independently verified
- **Type**: Combined multi-sheet set
- **Summary**: 3.7MB, could not be rendered in this environment. Very likely a merged PDF of all Project 288247 sheets above (M-001 through MP104).

### B01 E/01-22_Unit5.2_M11_1A.pdf
- **Area/Floor**: Unit 5 / LCC (Bioinformatics), 1st Floor / crawl space
- **Type**: MH ductwork & piping part plan
- **Summary**: Crawl-space hydronic piping (heat exchanger, air separator, expansion tank, HWP-1/2, valves VW-16-30, ¾"-1½" HWS/HWR) plus 1st-floor ductwork (6" round to 32x12, VAV terminals, VFD note). Harriman Associates, HA Project 01129, sheet M11.1A, "AS-BUILT," plotted August 2003.

### B01 E/01-22_Unit5.2_M11_2A.pdf
- **Area/Floor**: Unit 5 / LCC, 2nd Floor
- **Type**: MH ductwork & piping part plan
- **Summary**: 2nd-floor steam/hydronic piping to offices/conference rooms, reheat valves VAV-14/20-30, new 1¼" steam tie-ins; ductwork 6"-24"/24x12, duct-chase detail, new fire dampers. Harriman Associates, sheet M11.2A, "AS-BUILT," plotted August 2003.

### B01 E/97-05-Unit 5.3-50_MD3_Demo.pdf
- **Area/Floor**: Unit 5, 3rd Floor
- **Type**: MD demolition plan
- **Summary**: 1997 renovation — removal of steam/condensate lines, relocation of exhaust ductwork. Harriman Associates, degraded photocopy scan; equipment tags not legible beyond demo notes.

### B01 E/97-05-Unit 5.3-53_M103.3rdDuct.pdf
- **Area/Floor**: Unit 5, 3rd Floor
- **Type**: MH ductwork plan
- **Summary**: Corridor-fed VAV layout, VAV boxes VW-4 through ~VW-17, duct 10"x8" up to 30"x12"/28"x12", static-pressure/humidity sensors, relocated exhaust riser. 1997 project, poor scan quality but mostly readable.

### B01 E/97-05-Unit 5_T101.pdf
- **Area/Floor**: Unit 5, all floors
- **Type**: Cover sheet / drawing index
- **Summary**: Cover sheet for "Renovation of Main Building Unit 5," Harriman Associates, issued 6-13-97, addendum 9-8-97. Lists full drawing set (architectural, HVAC demo/ductwork/piping for 1st-3rd + penthouse, electrical, structural) — index tying together MD3/M3, M103, etc.

### B01 E/Mechanical.pdf
- **Area/Floor**: Unit 5 Bioinformatics (1st-3rd + roof) and adjoining Unit 4 (3rd floor + mech roof)
- **Type**: Full mechanical set — legend, demo, ductwork, piping, details, schedules (18 pages)
- **Summary**: WBRC, JAX project 2882.63, "Issue for Bid" 07.21.10 (ASI-010 rev 01.28.2011). VAV-501-508, AHU-1E (90-1220 CFM), Unit 4: AHU-1E/2E/3, CU-E, EF-E, chilled water (ECWS/ECWR), AFCV-1 fume-hood control valve (Microchem Lab, 725-2600 CFM). M-601 schedules: VAV-101 through VAV-303, AHU-3 at 10,000 CFM McQuay.

## Building 03

### B03/B03_TrainingLab-CDSET_20230217 M01.pdf
- **Area/Floor**: Training Lab area (Animal Holding 1040, Training Lab 1030, Corridor 1035, Peel rooms 1040A/B/D)
- **Type**: M demo + proposed ductwork plan
- **Summary**: Removal of reheat coil/humidifier/fume hood connection; new humidifiers H-1030/H-1040, reheat coil RH-1040, portable PIV rack ductwork. CFM tags 55-480. JAX Facilities Engineering, sheet M-01, dated 2/17/2023.

### B03/B03_TrainingLab_MECHALL.pdf
- **Area/Floor**: Training Lab (same area)
- **Type**: Proposed ductwork plan
- **Summary**: Expanded/updated version of the CDSET sheet, revised 9/20/2023 — adds PH-1, CC-1, existing CU-1, ATC panel, duplex condensate pump. Same CFM range (40-480).

### B03/Building 3 Duct work.pdf
- **Area/Floor**: Whole building overlay
- **Type**: H (HVAC overlay) plan
- **Summary**: Color-coded supply (green)/exhaust (blue) overlay, diffuser CFM tags (50-280), existing equipment "(E)" tagged (CC-1(E), SF-1(E), FH-1(E)), MVD/VD dampers. TJL design, dated 09.19.07, rev 01-09-08. No formal schedule — routing overlay only.

## Building 06

### B06/288243-M-101 M-101 NKB GRH comments.pdf
- **Area/Floor**: D-1 Renovations, 1st floor (Animal Room, Peel rooms, MEEL, mech room)
- **Type**: M plan, redlined review copy
- **Summary**: WBRC project 2882.43, CD 4/15/05, rev. through 02/24/06. Heavy redline markup over existing ductwork (12x8(E)-34x12(E)), new 1¼" HWS/HWR, AHU-1 plenum tie-in, EF-3 (190 CFM), 36x12 exhaust louver, portable PIV (40 CFM ea).

### B06/288243-M-501 M-501 NKB comments.pdf
- **Area/Floor**: D-1 Renovations (schedules/details)
- **Type**: M schedules, redlined review copy
- **Summary**: Hot Water Reheat Coil schedule (RH-1/RH-2), Air Balancing schedule (~3415/3285 CFM total), Exhaust Fan schedule (EF-1 fume hood, TX12F), PIV Equipment schedule. Red markup present.

### B06/5-23-05/M-101-05.23.pdf
- **Area/Floor**: D-1 Renovations, 1st floor
- **Type**: M plan, clean as-built
- **Summary**: Clean counterpart to the NKB-comments M-101 — same layout, AHU-1, EF-3, relocated NuAire fume hood (863-300, 200 CFM), 36x12 exhaust louver.

### B06/5-23-05/M-101-05.23jax.pdf
- **Area/Floor**: D-1 Renovations, 1st floor
- **Type**: M plan, JAX-labeled as-built variant
- **Summary**: Near-duplicate of M-101-05.23.pdf with EG(E) CFM tags (40/70/100/165) — same layout, minor annotation differences.

### B06/5-23-05/M-501-05.23.pdf
- **Area/Floor**: D-1 Renovations (schedules/details)
- **Type**: M schedules, clean as-built
- **Summary**: Clean counterpart to NKB-comments M-501 — same Reheat Coil/Air Balancing/Exhaust Fan/PIV schedules, no redline markup.

## Building 12

### B12/09-11_2010RENO_Combine Record Drawings_M.sheets.pdf
- **Area/Floor**: Animal Room Renovations, Rooms 1130 & 1140 (1st & 2nd floor)
- **Type**: Combined mechanical set — legend, demo, ductwork, piping, details, schedules (10 pages)
- **Summary**: WBRC + Hewett & Whitney, Comm. 2882.61, dated 10.15.10. GI001/GI002 (index/symbols), M-001 (legend), MD101/102 (demo), MH101/102 (duct plans), MP102 (piping), M-501 (details), M-601 (schedules — values too small to read reliably).

### B12/12-AR1_91-38_HV1.PDF through HV8, MD1, P1-P3, T1
- **Area/Floor**: Building 12, "Animal Production Rooms," 1st & 2nd floor (mech room)
- **Type**: HVAC ductwork/piping/sections/details/schedules record set (1985)
- **Summary**: Harriman Associates / Lappin Bros. Incorporated record drawing set, dated Nov 30, 1985, "AS BUILT" certified by J. Slotnik Co. April 30, 1993. HV1=1st floor ductwork, HV2=2nd floor ductwork (+ exhaust fan/glycol tank support details), HV3/HV4=1st/2nd floor piping, HV5=sections (mech room/ridge room), HV6=schematic details (14 items — reheat coil, drip legs, converter piping, fire dampers, etc.), HV7=schedules (Unit Heater CUH-8/9, RGD S1-S4/E1-E2, Reheat Coil RH-1 through RH-10, Filter F1-F4, Exhaust Fan EF-1 through EF-4, Pumps HWP-1/2 & CHWP-1/2, AHU 1-2-3-4 [Trane Size D, "House Rooms," 10,000 CFM total], Room Pressurization schedule for House Rooms 130/140/150/160), HV8=utility vault/site entry details. MD1=2nd floor mech room demo. P1-P3=drainage/supply/mech-room plumbing. T1=title sheet/drawing index (confirms full set: T-1, SD-1, D-1, A2-A7, S1-S3, P1-P3, HV1-HV9 [HV9 not in this folder], E1-E4).

### B12/B12 LEVEL1 12_Current.pdf / B12 LEVEL1 12_grid_Current.pdf
- **Area/Floor**: Building 12, Level 1
- **Type**: Architectural base plan (no mechanical content) / same with structural grid overlay
- **Summary**: Room layout (1130, 1140, 1145, 1150, 1160, 1165, 1180, 1185, 1900E + subdivided rack rooms). Grid version adds column lines 1-13 and a "B51" callout — matches the grid used in the Hduct model files below. No title block/date on either.

### B12/Hduct_ bldg12 Model (1).pdf and (2).pdf
- **Area/Floor**: Building 12, Level 1
- **Type**: HVAC ductwork model export/diagram (uncertified working drawing)
- **Summary**: Color-coded duct routing (blue supply, orange diffusers) over the same grid as the floor plans above; duct sizes 22x16, 28x12, 18x8, 14x6; PIV references, "EXISTING DUCT TO REMAIN" note. Model (2) is a simplified/companion version with fewer annotations. No title block/stamp/date on either — treat as coordination sketches, not record drawings.

### B12/Shop Drawings/ (18 files, mostly labeled "20-ARL_91-38")
- **Area/Floor**: Mixed — see Known Issues; title blocks mostly read "Building 12," a few read "Animal Production Rooms and Receiving" (Bangor Roofing & Sheet Metal Co.)
- **Type**: Structural steel shop drawings (01-03), fire protection shop drawings (FP1-FP4), mechanical composite coordination drawings (M1-1 through M5-1), plumbing composite coordination drawings (P1-1 through P3-1)
- **Summary**: 01-03 are structural steel erection/anchor-bolt drawings (Portland Steel Inc., ~1993-94) — not mechanical. FP1-FP4 are Noremac Sprinkler Corp. fire sprinkler piping plans (~1993-94) over a repeating small-room grid (animal holding pattern). M1-1/M1-2/M2-1/M2-2 are composite HVAC duct/pipe/plumbing coordination plans over the same room grid, dated 12/9/93, stamped "RECORD DWGS." M3-1 is a mechanical schedule sheet (unit heaters RH-1 through RH-10, reheat coils, filters, AHU, exhaust fans, RGDs). M3-2/M4-1/M5-1 are utility-vault piping, 2nd-floor mech-room equipment plan (HHW supply/return, large AHU/coil footprints), and 16 schematic piping details. P1-1/P2-1/P3-1 mirror the M-series as plumbing composite plans. Most fine-print equipment tags/values are too small/dense to transcribe reliably from these 1993-94 scans.

## Building 15 / Building 18

### B15/00-05_T24Relo_2882_16_E3_Schedules.pdf, 00_15_T24Relo_2882_16_E2_ELEC_PWR_PLAN.pdf, 2882_16_ELEC_LTG_PLAN.pdf
- **Area/Floor**: Trailer #24 Relocation project ("T24 Relo"), project 2882.16
- **Type**: Electrical schedules / power plan / lighting plan
- **Summary**: Panelboards SP-3 (existing) and MH (new modular, 120/208V 100A), lighting fixture schedule, electrical equipment schedule (autoclave/refrigerator/hoods/incubator), PIV alarm wiring. Power plan shows PA system, fire alarm panel, existing AHU-1, 75kVA/15kVA transformers, panel MH circuits MH-2 through MH-34. Dated MAR 29 2000, sheets 12-14 of 14, rev 1 dated 11/13/00.

### B15/00-05_T24Relo_2882_16_M2_Schedules.pdf, 2882_16_M1_MECH_PLAN.pdf
- **Area/Floor**: T24 Relo project
- **Type**: MH details/schedules and ductwork/piping plan
- **Summary**: Split system (Mitsubishi), steam humidifier (DRI-STEAM ULSV-3, 100#/hr), reheat coils RH-1/RH-2 (Trane, 2400/500 CFM), EF-1 fan. Ductwork plan shows section through trailer/mouse room roof, steam/condensate tie-ins to existing AHU-1, duct sizes 24x12-20x10, ~300 CFM branches, new 20x20 exterior supply duct. Dated MAR 29 2000, sheets 10-11 of 14.

### B15/04_19_AX1 _RENO-M-1.pdf
- **Area/Floor**: Annex 1 (AX1) Renovations, JAX Job 04-19/EPN 2004-19 — separate later project from the T24 Relo and original AX1 projects
- **Type**: Mechanical (domestic hot water/heating) demo + proposed plans
- **Summary**: Demo of ceiling diffusers/pneumatic sensors/sink-shower fixtures; new DHW piping, radiant ceiling panels, JCI VG7241E controls. "AS-BUILT," dated 07/08/04.

### B15/99_ax1_2882_AN1_M1_Ductwork.pdf, M3_Schedules.pdf, M2 Layout1 (1).pdf
- **Area/Floor**: Annex #1, "JRS Expansion – Phase 1," project 2882.02 (original/earlier Annex 1 project)
- **Type**: MH ductwork plan, schedules, mech room plan/sections
- **Summary**: Animal-room ceiling ducts 10x10(E)-24x24(E), new 8" HWS/HWR, rebalance to 332/158 CFM. AH-1 (Trane TSCH-21, 6300 CFM, 5.8HP), AH-3 (Trane TSCH-14, 6300 CFM). Sequences of operation; AHU-1 elevation/section, CWS/CWR/HWS/HWR tie-ins, duct smoke detectors, isolation dampers. Dated 27 AUG 1999, 8-sheet set.

### B15/combined.pdf
- **Area/Floor**: Building 15 — both T24 Relo (2882.16) and AX1/JRS Expansion (2882.02) projects
- **Type**: Merged 9-page PDF
- **Summary**: Concatenation of the 9 other B15 files above in sequence — no new content.

### B18/Jackson Labs Library Reno Control Submittal Package (1).pdf
- **Area/Floor**: JAX LCC Library Renovation + Unit 4 (equipment tags share "-18" suffix, e.g. AHU-1-18)
- **Type**: Controls (BAS/temperature-controls) submittal package — 127 pages, too large to fully render (22.8MB)
- **Summary**: Front matter (via bookmarks): Letter of Transmittal, Valve Schedule, Network Riser, Hot Water Flow Layout, AHU-EF #1&2 Flow Layout, AHU/EF-18-1 Sequence of Operation, VAV Supply & Exhaust Flow Layout, Supplemental Heating Sequence, CUH Flow Layout, Wiring Details, AMS Schedule, Room Schedule — followed by ~85 pages of vendor cut sheets. Ties to the 2018 WBRC "JAX LCC Library Renovation" project below.

### B18/MECHANICAL Pages from 2018_05_03 - JAX LCC and Unit 4 Con Docs.pdf
- **Area/Floor**: JAX LCC Library Renovation + Unit 4, Bar Harbor
- **Type**: Full mechanical set (legend, demo, new-work, enlarged plans, details, schedules)
- **Summary**: WBRC, project 2882.80, 100% CD dated 03 MAY 2018. M-001 legend; MD101/102/112 demo (LCC 1st/2nd, Unit 4 2nd); M-101/102/112 new plans (hot-water finned-tube radiation, convectors, VAV boxes replacing steam radiation); M-401 mech room (AHU-1-18, HX-1-18, P-1-18/P-2-18); M-501 details; M-601 schedules. Tags: AHU-1-18, EF-1-18/2-18, CU-1-18, VAV-1-18 through ~13-18, CUH-1-18/2-18, CONV-1-18 through 4-18, XT-1-18.

## Building 19

### B19/01-23_MH101-1_3rd_PH1Ductworkpdf.pdf
- **Area/Floor**: Building 19 (MGL), 3rd Floor (Phase I)
- **Type**: MH as-built ductwork plan
- **Summary**: Mouse rooms 3610A-F, procedure rooms off 3600/3860, duct 10x6-22x12/10x12/16x14, existing UH-3 to remain, Ebtron 3000/3110 airflow station. SMRT, Project 20113, sheet MH101-1, "As-Built 12-30-02."

### B19/01-23_MH101-2_2nd_PH2Ductwork.pdf
- **Area/Floor**: Building 19 (MGL), 2nd Floor (Phase II)
- **Type**: MH as-built ductwork plan
- **Summary**: Mouse rooms 2610A-2630F off 2600/2860, existing 12x10 ducts, 22x12/10x6 branches, bathroom exhaust to remain. Same project, sheet MH101-2, "As-Built 12-30-02."

### B19/01-23_MH111-1_PH1_pent_ductwork.pdf
- **Area/Floor**: Building 19 (MGL), Penthouse (Phase I)
- **Type**: MH as-built ductwork plan/elevations
- **Summary**: Grid J1, AC-5 connection, filter banks #3-6 in risers, duct up to 50x24/36x24, exhaust fan discharge. Sheet MH111-1, "As-Built 12-30-02."

### B19/MH111-2_PH2_pent_ductwork.pdf
- **Area/Floor**: Building 19 (MGL), Penthouse (Phase II)
- **Type**: MH as-built ductwork plan + details
- **Summary**: Relocated RHC-4/RHC-5, HU-4/HU-5 in vertical 22x12 supply duct, 48x18/60x16 sections; isometric humidifier and hot-water coil piping details. Sheet MH111-2, "As-Built 12-30-02."

## Building 20

### B20/007-B20_ARL_76-10-H-3.PDF
- **Area/Floor**: "Research Animal Facility," typical 1st & 2nd floor
- **Type**: Legacy mechanical duct riser/shaft section drawing
- **Summary**: Small key plan (new animal lab addition vs existing lab), vertical shaft sections (North/Center/South) at 1st/2nd floor ceilings, two wall-section details. Date/job number largely illegible — old-vintage drawing.

### B20/02-32_RAF8_MH101_RECORD MH101 (1).pdf
- **Area/Floor**: Building 20, Levels 2 and 3
- **Type**: MH ductwork plan (conformed record set)
- **Summary**: "BLDG #20 RAF-8 Renovations," WBRC, Conformed CDs dated 05/19/06 (project 2882.42). Colony Rooms, Procedure Rooms #1-4, VAV-E/VAV-P terminals, exhaust grilles EG-1 through EG-4 (~75-500+ CFM), duct to 84x24E/36x24E, AFMS at PIV supply detail.

### B20/20200511.B20-B6 Renovations.Drawings.IFB.pdf
- **Area/Floor**: Building 20, Level 2, Room B6 (RAF)
- **Type**: Full multi-discipline renovation set, Issue For Bid (21 sheets, all read)
- **Summary**: SMRT, Project 20537, IFB 05-08-20. Rooms 2825/2825A-F, Holding 02.06. Architectural, FP, Plumbing, Mechanical (M-001, MH101/102, M-501/601), Electrical. Mechanical: E-1 (360 CFM), S-1 (200 CFM), S-2 (300 CFM) to PPIV racks; Penthouse plan references existing AHU-1A/1B, ducts to 84x24E/78x26S. Schedules: Humidifier H-1-4 (2850/1840 CFM), Reheat Coil RHC-1-4 (2850 CFM, 61.8 MBH), VAV SAD-1 (2020/1840 CFM), EAD-1 (1170/980 CFM), EAD-2 (880 CFM).

## Building 21 (Snell / BRL)

### B21/18-76_21_2305_M01_10.19.2018_ASBUILT.pdf
- **Area/Floor**: 2nd floor, rooms 21-2295 through 21-2306
- **Type**: Existing/removals + proposed ductwork plan (as-built)
- **Summary**: "AS BUILT 10/19/2018." Removed VAV, isolated 21-2306; proposed 500 CFM VAV to 3x140 CFM diffusers, 8"x16" oval duct, ductless heat pumps/fumehood, condensing unit locations. Duct sizes 16/10, 16/12, 14/8, 12x8, 10/6, 12" round.

### B21/MD-100Demo and 1stfloor.pdf
- **Area/Floor**: 1st floor part plan / 2nd floor demolition
- **Type**: MD demolition plan
- **Summary**: "Snell Building 2nd Floor Renovation," Allied Engineering, dated 10/14/2019, rev 4 (12/19/2019). Removal of ductwork/diffusers/heating coils/HWS&R piping, relocation of AFCU-21-2305-1 and a VAV box.

### B21/MH-100_SecondFloor.pdf
- **Area/Floor**: 2nd floor (Mammalian, Bacteria, SER, Cell Sorting, Analysis, Clean Prep, Instrument, MAS, Histology)
- **Type**: MH ductwork + piping plan
- **Summary**: HWS&R, PVDF fume exhaust, control valves; supply/exhaust grilles at 110-1030 CFM, VAV boxes, 12"ø exhaust risers to penthouse, O2 wall sensor. Same reno set, rev through 12/19/2019.

### B21/MH-101_PenthouseRoofPlan.pdf
- **Area/Floor**: Upper/lower penthouse and roof
- **Type**: Mechanical penthouse/roof plan
- **Summary**: Fume/histology hood exhaust ducts (12") through roof w/ gooseneck, removal of EAV-19-21, existing condensing units to remain in lower penthouse.

### B21/MH-500/501/502 (Details and Notes / Schematics Details)
- **Area/Floor**: Not floor-specific
- **Type**: Details/schematics sheets
- **Summary**: MH-500: radial diffuser, reheat coil connection, air measurement station, humidifier piping, fire damper, VAV schematic. MH-501: duct port near sensors, AHU condensate piping, hydronic coil piping, pump & source exhaust piping (includes jobsite photos). MH-502: chilled water schematic (AS-1 separator, shot feeder), in-line pump, chiller piping ("to Chiller #2"), fan coil piping, expansion tank piping. All part of the 2019 reno set.

### B21/MH-600/601/602 Schedules
- **Area/Floor**: 2nd floor (all rooms)
- **Type**: Schedules
- **Summary**: MH-600: Basis of Design (per-room ACH/setpoints/exhaust CFM), Single Duct Air Terminal (SDV-11-21, SDV-12-21, SDEQ/SDE-5000), Duct Heating Coil (HC-15-21 through HC-23-21). MH-601: Fan Coil (FC-2380/2405A-B/2370/2350/2355/2330, MultiAqua), Hydronic Pump (CHWP-1/2-21), Electric Humidifier (H-1, DRI-STEEM), Air Cooled Chiller (CH-1/CH-2, MultiAqua 10-ton). MH-602: Air Measuring Station schedule (AFCS-/AFCE-/AFCFE- tags).

### B21/SKM-2 Revised HeatingCoilSchedule.pdf
- **Area/Floor**: 2nd floor renovation
- **Type**: Heating coil schedule revision sketch
- **Summary**: Updated HC-15-21 through HC-23-21 schedule (revisions to MH-600/A1). Allied Engineering, project 18070, dated 04/10/2019.

### B21/Viral vector plumbing as-builts.pdf
- **Area/Floor**: Unknown — could not open (29.8MB, exceeds render limit)
- **Type**: Likely plumbing/exhaust as-built for a viral-vector lab — unverified
- **Summary**: Content not confirmed in this pass; see Known Issues.

### B21/Renovation Plans/21_2305.GT_20180803_M01.pdf
- **Area/Floor**: 2nd floor, rooms 21-2295 through 21-2306 (pre-construction draft)
- **Type**: Existing/removals + proposed ductwork floor plan, draft
- **Summary**: Earlier draft (design date 8/3/2018, drawn by J. Murray) of the same M01 as the 10/19/2018 as-built above — omits the ductless heat pump/fumehood/condensing unit notes added later.

### B21/Old/ (superseded set — see Known Issues)
- **55.First FloorM.Duct.pdf**: 1st floor, "wing 55" corridor/lab area — duct 24x18S/E, 20x12S, 18x10E, 16x10S; HWS&R tie-ins; no date visible, likely historical/superseded.
- **B21.1.ViralVectorDuctwork.pdf**: Ground/basement mechanical & utility corridor — dense multi-color piping overlay, central mech/boiler room; no title block visible; likely superseded by the current "Viral vector plumbing as-builts.pdf."
- **MH-100 (2nd/3rd floor part plans)**: "Snell Building 3rd/4th Floor Renovation," Allied Engineering, Project 14011, ~Sept 2014 — existing ductwork to remain (2nd fl), new/relocated risers (3rd fl).
- **MH-101 (4th floor & lower penthouse)**: AHU-1-21/EAHU-1-21 relocated 4th-floor AHU; supply/exhaust to 4100 Lab, 4205 Admin, 4470 Prep; viral vector general supply/exhaust 3150/4130 CFM.
- **MH-102 (upper penthouse)**: Large exhaust/supply mains (70x32E-72x42E / 40x22S-50x46S) feeding riser drops; histology fume hood exhaust 1500 CFM.
- **MH-103 (roof plan)**: AHU-1-21/EAHU-1-21 rooftop unit, CU-1-21, 22"-ID exhaust stack; vertical chase section 1st floor through roof.
- All Project 14011, "Issued for Construction — September 09, 2014" (also marked "Not For Construction" — conflicting stamp), filed under "Old" as superseded.

## Building 28 / Building 29

### B28/28 2nd floor.png
- **Area/Floor**: 2nd floor
- **Type**: Architectural space plan (not a duct print, despite being filed here)
- **Summary**: Room layout image — open offices, Training 2325, Laboratory 2310, Animal Husbandry 2255, Café 2025, Mech Plenum 2055A. No ductwork/CFM shown.

### B28/B28 VAV Box Locations.pdf
- **Area/Floor**: 2nd floor
- **Type**: Hydronic piping plan (filename says "VAV Box Locations" but content is piping)
- **Summary**: "Building 28 Second Floor Renovation," Harriman Project 20500, CD dated August 26, 2021. Locates VAV-1 through VAV-28, B28-AHU1/EAHU1, pumps P-1/2/3; HW/baseboard piping ¾"-4", CHW, LP steam/condensate, heat-recovery piping with GPM totals.

### B28/B28.1_MECH_OverlayDuctwork_2019.COLOR.pdf
- **Area/Floor**: Level One
- **Type**: Color-coded ductwork overlay/compiled record drawing
- **Summary**: "Building 28 Heat Recovery" project, JAX Facilities Engineering, dated 07/11/2019. Cyan=supply, orange=exhaust, blue=other. Rooms 1000-1390, duct 8x6 to 48x24, rebalance CFM setpoints noted at many diffusers. Sourced from a 2009 Allied Engineering drawing — "accurate as of around 2009."

### B28/M10-2-SECOND-FLOOR-DUCTWORK-Rev.4.pdf
- **Area/Floor**: 2nd floor
- **Type**: Renovation ductwork plan, Construction Documents
- **Summary**: Same 2021 renovation (Harriman Project 20500) as the VAV Box Locations sheet. Duct 12x14 to 30x14 (S and E); notes for future supply/exhaust AHU floor space, existing AHU reconfiguration/warehouse conditioning during phasing.

### B29/005-B29_AR3_90-06-HV1 through HV5
- **Area/Floor**: Building 29, Animal Production Building, Annex 5 & 6
- **Type**: HVAC ductwork/piping/sections/details/schedules (circa 1990)
- **Summary**: Harriman Associates. HV1=full floor plan (rack rooms, holding rooms, cage-wash, House Room, duct 30x12/27x12). HV2=mech room part plan + sections (heavily hand-redlined). HV3=building sections, control diagram, flash tank detail. HV4=piping/equipment detail sheet (no room-specific tags). HV5=schedules (EF-1 through EF-4, RH-1 through RH-8) + piping details.

### B29/13074_MH-100.pdf, MH-101.pdf, MH-500.pdf
- **Area/Floor**: Title blocks read "Building 31 (Annex 10)" / "Building 32 (Annex 11 and 12)" — filed under B29 (see Known Issues)
- **Type**: MH ground-floor duct plan / duct plan + mech specs / spec-only sheet
- **Summary**: "Renovations to B31 & B32 - Annex 10, 11, 12," Design Group Collaborative/Allied Engineering, Review Set 29 Aug 2013 ("Not For Construction"), Project 13074. Mirrored Holding Room #1/#2 wings, central mech room, duct 30x12 SA/36x16E existing. MH-500 duplicates the MH-101 spec page rather than containing unique content.

## Buildings 30-32 / Building 33

### B30-32/008-B30AR4_31AR5_32AR6_91-36_HV1-5
- **Area/Floor**: Buildings 30, 31 & 32 (AR4/AR5/AR6 annex designations)
- **Type**: HVAC drawing series, job 91-36 — content NOT verified
- **Summary**: No extractable text layer and no PDF rasterizer available in this pass; sheet-by-sheet content unconfirmed. Re-catalog with proper tooling before relying on this.

### B30-32/01-20_AX7_M-101-M-101.pdf
- **Area/Floor**: Annex 7 (AX7), Job 01-20/EPN 2882.20, sheet A7
- **Type**: Mechanical floor plan (renovation)
- **Summary**: Rodent surgical/gowning suite — Mouse Room, Mech Room 12, Surgical Suite 11, gowning corridor (Clothes/Shoes On/Off, Toilet, Entry/Exit Lock). Remove ductwork drops to mouse racks and cap; new exhaust grille in Surgical Suite 11 (8"x6" Anemostat X35HS), balance to 150 CFM total. Existing ducts 6x6(E)-14x10(E).

### B30-32/13074_MH-100.pdf, MH-101.pdf, MH-500.pdf
- **Area/Floor**: Not confirmed — job 13074, no building reference in extractable text
- **Type**: Mechanical/HVAC sheets — content NOT verified (no text layer, no rasterizer)
- **Summary**: Same job number as the B29-filed 13074 sheets above (Building 31/32 Annex project) — likely related but not directly confirmed for this folder's copies.

### B30-32/15-02_20150211.ANNEX 9.MEP DD REVIEW SET.pdf
- **Area/Floor**: Annex 9
- **Type**: MEP Design Development review set, job 15-02, dated 2015-02-11 — content NOT verified
- **Summary**: 6 pages, no extractable text layer, not rendered in this pass.

### B33/B33.pdf
- **Area/Floor**: Building 33 (NRB) — content NOT verified
- **Type**: Multi-sheet mechanical/duct print set, 24 pages
- **Summary**: No extractable text layer, not rendered in this pass. Page count suggests a fairly complete building-wide mechanical set.

## Building 50 (GRB)

### B50/08-13.L1_PEEL.PIV.Renovation/Construction PDFs - Part 1.pdf
- **Area/Floor**: Level 1 — "PEEL" spaces 50-1050 through 50-1060C, Fixed PIV Rack rooms 1210/1230
- **Type**: Full CD set (architectural/mechanical/plumbing/electrical), 14 pages
- **Summary**: "Fixed PIV Rack Conversion — Rooms 1210 and 1230 and First Floor PEEL Conversion," Allied Engineering + HKTA, Project 10029-3, dated 03-30-2012. A-102 through A-106 legible (RCP, door schedule, details, finishes, caulk schedule); mechanical/plumbing sheets have no extractable text in this pass.

### B50/10029_MH-101.pdf = B50/B50 groud floor.pdf (duplicate, see Known Issues)
- **Area/Floor**: Ground Floor / Level 1 Interstitial
- **Type**: MH mechanical part plan
- **Summary**: "Mechanical Part Plan — Ground Floor Interstitial," Building 50 Level 1 Renovations Phase II, Allied Engineering, dated 03-29-2011.

### B50/13-21_B50.1255.Renovation/Revision 1 11-15-2013 PDFs.pdf
- **Area/Floor**: 1st floor room 50-1255 (converted to Janitor 50-1255B) + 1st floor interstitial
- **Type**: Full CD set, Revision 1 — 10 pages
- **Summary**: "Room 50-1255 Upgrades," Allied Project 13038, HKTA + Allied Engineering, rev dated 15 Nov 2013. A-100 (demo/elevations), P-000/P-100 (plumbing legend/plans), M-100 through M-104 (demo, part plans, EAV-50-3P through -9/SAV-50-3P through -10 schedules, ~300-2000 CFM, specs), E-100 (emergency lighting).

### B50/50-G.tif, B50/B50 groud floor.tif — could not open (binary TIFF, no reader available)
- **Area/Floor**: Ground Floor (per filename) — unconfirmed
- **Type**: Unknown scan

### B50/50.1_DUCTWORK_DRAFT20200319.pdf
- **Area/Floor**: 1st floor
- **Type**: HVAC duct shop drawing (as-built/redline draft)
- **Summary**: Sheet SM-03, Northeast CAD for Ranor Inc., base dated 04/06/1999, rev history to 04/08/2020 (Rev 5). "Changed Ductwork" vs "Original Ductwork" overlaid on 2020 floor plan, rooms ~1015-1285.

### B50/50.Pent_H2.4_ductwork.pdf = B50/B50 3rd floor.pdf (duplicate, see Known Issues — both are actually the Penthouse plan)
- **Area/Floor**: Penthouse / interstitial above 3rd floor
- **Type**: HVAC ductwork plan
- **Summary**: Sheet H2.4, "Third Floor Fit-Out HVAC Penthouse Plan," Einhorn Yaffe Prescott, dated 12/12/2000, rev 1 01/21/2002.

### B50/B50 G floor Overlay.bmp (unreadable) / .jpg (readable)
- **Area/Floor**: Ground Floor
- **Type**: Overlay image (room numbers + duct/equipment layout)
- **Summary**: JPG (5736×4232px) shows room callouts (G155, G145, G135, G250A autoclave, ELB060/070, stair B330) over ductwork/equipment graphics — working reference image, not a stamped drawing.

### B50/FirstFloor_GRB-50-AS BUILTS_M.PIPE_ranor_C-10.pdf
- **Area/Floor**: 1st floor
- **Type**: Mechanical piping as-built plan
- **Summary**: Sheet C-10, Northeast CAD for Ranor Inc., base dated 06/30/2000, rev to ~04/2006. Rooms 1015-1285 with cage/box-count annotations (Room 1210: 960 boxes; 1230: 1320; 1255: 1920) — likely PIV rack sizing basis. Title-block text renders mirrored (scan artifact).

### B50/JAX.Allied.Compiled.Ductwork_B50.L1.pdf
- **Area/Floor**: Level 1
- **Type**: Compiled ductwork/piping reference drawing
- **Summary**: JAX Facilities Engineering, color-coded (blue/orange/cyan) compiled Level 1 duct drawing, sourced from Einhorn Yaffe Prescott as-builts H2.1/H2.2 (M3-a.dwg) for internal reference.

### B50/JAX_M3-A_3rdFloor_HVAC.pdf
- **Area/Floor**: 3rd floor, Area A
- **Type**: HVAC plan
- **Summary**: Sheet H2.1, "Third Floor Fit-Out HVAC Plan — Area A," Einhorn Yaffe Prescott, dated 12/12/2000, rev 1 01/21/2002. RF-shielded room, duct drops, blast gates, DP sensors for animal-holding rooms. Companion to H2.4 (Penthouse Plan above) and source for the compiled drawing.

### B50/JAX_M3-A_NOTES.pdf
- **Area/Floor**: Level 1 Interstitial Space
- **Type**: Ductwork/piping plan with legend + keyed notes (full plan sheet, not text-only)
- **Summary**: "B50 Level 1 Interstitial Space Ductwork/M.Piping" — symbols legend + notes on fire dampers, ceiling duct drops, sensors, manual volume dampers. Companion/legend sheet to the M3-a.dwg-derived drawings.

## Building 51

### B51/02-08-B51_L2_M2.2_Ductwork.ASBUILT.pdf
- **Area/Floor**: 2nd floor (Level 2)
- **Type**: Mechanical piping/ductwork as-built plan
- **Summary**: Sheet M2.2, WBRC, Project 2882.33, "As-Built Set" plotted 12/2003 (rev.1 02/20/2002 through rev.4 11/2003 as-built). Admin/office areas, corridors, stairs A/B; VAV box schedule VAV-1 through VAV-14.

### B51/MH101.pdf
- **Area/Floor**: 1st floor
- **Type**: HVAC plan (renovation/construction set)
- **Summary**: "Building 51 First Floor Renovation," WBRC, Project 2882.44, "For Construction" 4/28/2006. Animal-holding rooms 1300-1391, VAV boxes, PIV racks, sterile mats/clean corridors, stairs A/B; ceiling exhaust, VHF duct ports, motorized dampers, future fume hood provision.

## Building 53 (ERB)

### B53/07042 BSL2 upgrade.pdf / B53 07_40_B53.1_BSL2-MP_Sheets.pdf
- **Area/Floor**: Ground floor Lab G107 (+ related 1st/2nd floor sheets)
- **Type**: BSL2 upgrade — mechanical/plumbing pricing/construction set
- **Summary**: HKTA + Allied Engineering, "Updated Pricing Set — Issued for Final Review 05-23-2007," Project 07042, "BSL2 Laboratory ~ Building 53." VVS-G107-1/VVE-G107-1 VAV boxes (Enviro-Tec, 1240-1300 CFM), EF-G107-1 (Cook ACRUD-XP-195RX15D, 1300 CFM), tie-in to campus BAS (N2/VMA). The BSL2-MP file is a fuller 12-sheet superset adding PL-100/101 plumbing (CO2, vacuum, DI water).

### B53/53.1_ShopDrawing_Sheetmetal.pdf, 53.2_..., 53.G_...
- **Area/Floor**: Level 1, Level 2, Ground
- **Type**: Sheetmetal shop drawings (ductwork)
- **Summary**: Johnson & Jordan Mechanical Contractors / Einhorn Yaffee Prescott, drawn 11/03/03, as-built markups added 02/28/06. Color-coded supply/return/exhaust routing per floor. 53.G notes "G105 Office ductwork not shown" / "G111 BSL Lab ductwork not shown" — that scope documented separately in the BSL2 upgrade set.

### B53/B53.zip — duplicate archive, see Known Issues (contains the 5 files above)

## Building 55 (FGB)

### B55/55 3925 reno.pdf
- **Area/Floor**: 3rd floor
- **Type**: ABSL-2 renovation ductwork demo & new work
- **Summary**: "RAF-MNBF(B01) & ABSL-2(B55) Renovation," Harriman, Project 12762, Record Drawing rev 3 dated 05-19-15. Duct 30x12-14x8, fume hood exhaust ~600 CFM/hood, gas-scavenging PVC piping, wash-down zone sensors, exhaust to penthouse.

### B55/55.2_SM02, 55.3_SM03, 55.4_SM04 Sheetmetal
- **Area/Floor**: Floor 2, Floor 3, Floor 4
- **Type**: Sheetmetal shop/record drawings
- **Summary**: H.E. Sargent Inc. Floor 2 (dated 12/08/03): vivarium dirty/clean corridor layout, rooms 2700-2940. Floor 3 (2/18/04): similar layout, rooms 3700-3990. Floor 4 (2/18/04): imaging/phenotyping suite, RF-shielded room (MRI-adjacent), rooms 4400 range.

### B55/55.First FloorM.Duct.pdf
- **Area/Floor**: 1st floor
- **Type**: Mechanical/piping plan (labeled "M.Duct" but mostly piping)
- **Summary**: Dense color-coded piping across central plant/boiler room (1010-1040) and zones 01A/B/C, 20, 21, 22, 53, 55. Title block/date not visible in this pass.

### B55/JAX B55 2_HVAC_EYP JX2-HB02-P.pdf
- **Area/Floor**: Floor 2
- **Type**: HVAC design sketch (in-house)
- **Summary**: JAX sheet SK-1 on EYP architectural background, revised 06/11/2013. 2900-series office/lab rooms, VAV/terminal units, CFM ~50-1780 — internal rebalancing/redesign sketch.

### B55/SM-05_55.5-Ductwork.ShopDrawing.pdf
- **Area/Floor**: Mechanical Penthouse (Room 5000)
- **Type**: Sheetmetal shop/record drawing
- **Summary**: H.E. Sargent Inc., dated 06/04/04. Large AHU duct mains (up to 42x24), OA louver, VAV box, coil-pull clearance — feeds the Floor 2-4 systems above.

### B55/TJL Bldg 55 As-builts 0011.pdf — likely duplicate of a Pricing Set sheet, see Known Issues

### B55/TJL_B55_COMP SCIENCE_Pricing Set_082214.pdf
- **Area/Floor**: Floor 2, rooms 2513-2517
- **Type**: Pricing set (architectural + mechanical + electrical)
- **Summary**: 15-sheet "For Pricing — Not for Construction," dated 08/22/2014, Project 14068/124016, Design Group Collaborative + Allied Engineering. MD-100, MH-000/100/500 with VAV S92A (Price SDV-5000, 800-1150 CFM) serving office 2517E; E-000/ED-100/EL-100/EP-100 electrical. Open-office/lab-support renovation.

## Building 56

### B56/10040-MH-100.pdf
- **Area/Floor**: 1st floor
- **Type**: MH ductwork plan
- **Summary**: Animal holding/procedure/gown-on/air-shower/VHP suite (56-1010 to 56-1210), Mech Room 26. Register tags S1/103, S3/336, E3/206, S5/470 CFM. Allied Engineering, "TJL Repository Phase II Interior Fit-up," rev 1 dated 6/6/2013.

### B56/10040-MH-101.pdf ↔ B56/10040-MH-102.pdf — sheet-number swap, see Known Issues
- **Area/Floor**: 2nd floor/penthouse (56-2200) / interstitial level above 1st floor
- **Type**: MH plans
- **Summary**: "MH-101" file (internally sheet MH-102): AHU-1-56, AHU-2-56, EAHU-1-56, HC-2-56; smoke damper/electric actuator retrofits. "MH-102" file (internally sheet MH-101): large interstitial ductwork, AMS-1-56 through AMS-29-26/27-56 air measuring stations, heat-hood interlocks tied to door tronics timer.

### B56/10040-MH-400.pdf
- **Area/Floor**: Interstitial level (enlarged plan)
- **Type**: Enlarged MH ductwork plan
- **Summary**: 1/4"=1' blow-up of interstitial ductwork, same AMS tags as MH-101/102, duct 48x24S/60x36S/50x30E/34x18S.

### B56/10040-MH-500/501/502 Details
- **Area/Floor**: N/A (details)
- **Type**: Mechanical piping/duct details
- **Summary**: HW/glycol/CHW air separator & expansion tank piping, coil piping, steam relief/drip pan, AHU condensate, PRV station, fire damper section, register boot, branch takeoffs, HX/glycol run-around coil (AHU-1-56/AHU-2-56), autoclave steam hood drain.

### B56/10040-MH-600.pdf
- **Area/Floor**: N/A (schedules)
- **Type**: Mechanical schedules
- **Summary**: Basis of Design (room-by-room ACH/pressurization), Duct Heating Coil (HC-1-56 through HC-17-58), Heat Exchanger (HX1-56), Condensate Receiver, AMS schedule, Fan/Pump/RGD/Unit Heater/Direct Steam Bleed Humidifier, Steam PRV, Air Control/Flash Tank. "ISSUED FOR PRICING," dated 12/22/2010, rev 1 6/4/2013.

### B56/10040-MH102.pdf (no dash — distinct working file)
- **Area/Floor**: Mechanical/penthouse equipment room
- **Type**: Ductwork/piping plan
- **Summary**: Mech room layout, HX1-56, PRS-1/2, CHW (5" CHWS/CHWR), glycol (2½" GWS/GWR), HW (¾"), steam (4" HPS, 5" LPS), DCW/DHW, small SA/RA ductwork. No sheet number captured — possibly a working/redline copy.

### B56/56.Ductwork.Shaded.JPG
- **Area/Floor**: Interstitial/mechanical level
- **Type**: Shaded rendered overlay image (raster, likely Revit/CAD export)
- **Summary**: Top-down shaded view matching the interstitial ductwork/AMS tags in MH-101/102/MH-400.

## Building 59 (Data Center)

### B59/10028M MH-100.pdf
- **Area/Floor**: Basement + 1st floor (two part-plans, one sheet)
- **Type**: MH mechanical plan
- **Summary**: Data Center 2nd-floor fitout project. Existing equipment noted (E) to remain; new ductwork through data-center ceiling space. Allied Engineering + HKTA, Project 10028, dated 3/26/2010, "AS-BUILTS."

### B59/10028M MH-101.pdf
- **Area/Floor**: 2nd floor
- **Type**: MH ductwork plan
- **Summary**: Full 2nd-floor plan, VAV boxes, ducts 6"ø-8"ø branches up to 74x10S/42x10S/42x12S/49x14S, fire dampers, 18x12 exhaust louver. Same project, dated 3/26/2010.

### B59/10028M MH-102.pdf
- **Area/Floor**: Roof
- **Type**: Mechanical roof plan + details
- **Summary**: VTR/RD locations, roof-mounted packaged unit outline; details for humidifier duct distribution, condensate trap piping, CHW AHU hot-water coil piping (Alternates #1/#3).

### B59/10028M MH-103.pdf
- **Area/Floor**: 3rd floor
- **Type**: MH ductwork plan
- **Summary**: Duct sizes 16x12S, 36x16R; sleeves for future humidifier distribution; roof-mounted packaged unit outline (base bid) and Alternate #2 option. Note: printed sheet number on this file appears to read "MH-102" as well — verify against the source PDF directly (see Known Issues, similar pattern to B56).

### B59/10028M MH-500.pdf
- **Area/Floor**: N/A (schedules/details)
- **Type**: Mechanical schedules
- **Summary**: Gas-Fired Humidifier (Alt #1), VAV box schedule, Fan/Pump/RGD schedules, Radiant Panel schedule, Rooftop Unit schedule (Alt #1 base/alt bid), Boiler schedule. "Data Center 2nd Floor Fitout," dated 3/26/2010, "AS-BUILTS."

## Building 57 (Dining Commons / Health & Wellness Center)

This building has two distinct projects filed together: the original 2006-2007 "Commons Dining Facility / Health and Wellness Center" base-building construction (Allied Engineering + JSA Architects), and a 2024 Harriman "Public Area Upgrades and Staff Conference Renovation" (Project 23601). Several sheet numbers repeat across the two projects — check the date in the title block to tell them apart.

### B57/62_M05-1.pdf, 62_M10-1.pdf (2024 renovation, 1st floor)
- **Type**: M demolition ductwork plan / new-work ductwork plan
- **Summary**: Harriman, Project 23601, Conformance Set Oct 7 2024, rev 12-19/12-20-2024. Existing diffusers/split unit/ERV removal (M05-1); re-installed grilles/split unit, new 20x10-24x10 ductwork, 8x6/8x8 exhaust, corridor with toilets 1040-1042 (M10-1).

### B57/Combined Prints.pdf (2006-2007 base building, 37 pages, all disciplines)
- **Summary**: "Commons Dining Facility / Health and Wellness Center," Allied Engineering + JSA, dated May 4 2007. Full E/EL/EP/M/MH/MP/P set. Key tags: RTU-1 (Trane 50-ton, Dining Commons), RTU-2 (York 25-ton, Wellness Center), AHU-1 (Haakon, kitchen, 3500 CFM OA), B-1 through B-4 boilers (Lochinvar KBL 399), EF-1 through EF-10, VAV-1 through VAV-18. Note on MH-100: "This print has the wrong room numbers."

### B57/E-000, E-100, E-101_Site, E-102 (electrical, 2006-07 project)
- **Summary**: Legend/symbols; 2nd-floor lighting plan (Wellness Center rooms); site electrical (lighting circuits, handholes, donor sign); mechanical-equipment electrical connections + luminaire schedule.

### B57/EL-100, EL-101, EL-101.Level2 (electrical lighting)
- **Summary**: 1st floor lighting + basement inset, daylighting control zones, panel LCK schedule. 2nd floor lighting (large open room), luminaire schedule F2-F12/TK/H1/H2. EL-101.Level2: 2nd floor + basement office/patient-care lighting, feeder key, riser diagram (400A/75kVA).

### B57/EP-100, EP-101 (electrical power)
- **Summary**: 1st floor power plan — panel L1 (480/277V 400A) feeding RTU-1/AHU-1/EF-2-4, kitchen panels KP1/KP2 with per-appliance circuits. 2nd floor — RTU-2/EF-1-6/AHU-1 roof equipment, power riser (KP1-3, 112.5kVA/75kVA transformers, 240V 400A disconnect).

### B57/Lobby_E-100, Lobby_M-100
- **Summary**: Entry/lobby lighting (Vestibule 57-0900, video wall cabling to auditorium projection). Entry mechanical + sprinkler part plans (existing ductwork relocation near reception 57-0910).

### B57/MH-100.Level2, MH-100, MH-101.Roof, MH-101, MH-102.Roof.ph1 (2006-07 ductwork)
- **Summary**: 2nd floor ductwork (Wellness Center, ties to RTU-2). 1st floor + basement ductwork (kitchen hood, dryer exhaust — "wrong room numbers" note). Roof plan (RTU-1, exhaust fans, AHU to remain). 2nd floor ductwork to EF-3/EF-4, RTU-1/2 outline, "Constructed During Phase 1." Roof Phase 1 (AHU modification, coil removal, duct furnace, 25' OA/exhaust separation note).

### B57/MH-500.Level2, MH-500, MH-501, MH-600.Level2, MH-600 — sheet-number swaps present, see Known Issues
- **Summary**: Standard mechanical details (VAV schematic, fire damper, register boot, dryer venting, reheat coil piping) — Wellness Center phase and Dining Commons phase versions. Schedules: VAV-10 through VAV-18 (Wellness Center rooms), Boiler B-4, RTU-2 (York 25-ton, 9800 CFM OA); VAV-1 through VAV-9 (Dining Commons), DF-1 furnace, AHU-1 (3500 CFM OA), RTU-1 (Trane 50-ton, 18990 CFM), B-1/B-2/B-3 boilers.

### B57/MH100.pdf
- **Summary**: 1st floor + basement mechanical plan, kitchen/office/servery/dining ductwork (40x30 down to 18x12), basement domestic water heaters — same "wrong room numbers" note as MH-100.pdf.

### B57/MP-100.Level2, MP-100, MP-100underslab, MP-101 — sheet-number swaps present (MP-100↔MP-101), see Known Issues
- **Summary**: 2nd floor + mech room piping (HWS/HWR ¾"-2½" to Wellness Center spaces; boiler tie-in note). Underslab 1st floor piping (1" Type K copper). Detailed 1st floor + basement piping (fan coils FC-1/2/3, CO2 sensors to RTU-1, boiler HWR/HWS risers) — note "UNDER SLAB PIPING NOT IN THIS CONTRACT."

### B57/P-000, P-100_Level1, P-100_Level1notes, P-100_Level2, P-101, P-200_Level1, P-200_Level2, P-200_Level2_lockerrooms.etc, P-201, P-300 — several sheet-number swaps present, see Known Issues
- **Summary**: Plumbing legend; sanitary plumbing plans for 1st floor+basement (general notes, invert elevations) and 2nd floor (fixture schedule P-1 through P-8, locker room part plan); domestic water plumbing 1st floor (CW/HW/DHWR, gas fireplace line) and 2nd floor (locker rooms, trap seal primer detail) — a markup variant of the 2nd-floor sheet also exists; roof LP gas piping (2"LP to DF-1); kitchen sanitary/domestic part plan (grease waste, floor drains, LP gas regulator for propane tank).

## Building 64 (IIF)

### B64/11032M MH-100/102/400/500/600 Third Flr, MP-100 Third Flr
- **Area/Floor**: Third floor fit-up (Media/Serology Lab 3225, Central/Necropsy Lab 3230, Untested Animal Holding 3040, PCR Lab 3115, Extraction Lab 3125)
- **Type**: MH ductwork/roof/sections/details/schedules, MP piping — HKTA + Allied Engineering, Project 11032, drawn 7/29/2011
- **Summary**: MH-100: SAV1-64 through SAV13-64, EAV2-64 through EAV14-64, AMS-1-64, HC-1-64, H-1-64; 48"x36"x18" autoclave hood, BSC ventilated thimble, future 144/192-cage racks. MH-102: roof plan, EF-4-64/EF-5-64 existing to remain. MH-400: sections showing vertical risers, AMS-2/3/5/6-64 chain, basement piping (1" HPS/¾" HPR) up to 3rd floor. MH-500: standard details (VAV schematic, autoclave capture hood, humidifier drain pan). MH-600: AMS schedule, duct heating coil, RGD, VAV terminal, fan, humidifier schedules, Basis of Design by room. MP-100: HWS&R/LPS/LPR/HPS/HPR piping throughout 3rd floor.

### B64/MH100.pdf, MH101.pdf, MH102.pdf, MH104.pdf — original base-building set (WBRC Architects Engineers), distinct from the 2011 fit-up above
- **Summary**: Basement ductwork (fan/AHU symbols, tags not legible). 1st floor ductwork (VAV symbols, autoclave hood, hand-marked as-built revisions). 2nd floor ductwork (VAV terminals, fire/isolation dampers — shares sheet number "MH102" with the unrelated 2011 roof-plan sheet, different project). Roof ductwork (two large rooftop AHU/louver enclosures, elevator penthouse).

## MP22-23 (Modular Animal Housing)

### MP22-23/12-MOD_90-09_M2.pdf, M3.pdf
- **Area/Floor**: Modular unit level (no multi-floor designation)
- **Type**: Modular unit ductwork plan + details / schedules & legend
- **Summary**: Alberti, LaRochelle & Hodson Engineering, Job 90-09. M2: repetitive modular bays, small ductwork (6"ø, 8"x8"), diffuser details. M3: rooftop AHU (Trane), exhaust AHU, pump, preheat coil, steam humidifier, unit heater, diffuser schedules; expansion tank, louver/damper, circulator pump, steam piping details.

## Building 74 (CBA — Center for Biometric Analysis)

Two overlapping projects: the original CBA building (Harriman/E.P.S., ~2017-2018, Project 25016/15434) and the "Pod 3" expansion (Harriman, Project 15434, 2018, "Preliminary — Not for Construction" as of Feb 2018 progressing to a certified Sept 2018 TAB report).

### B74/019500-002 HVAC TAB Report and Air Flow Plan 2818.pdf
- **Area/Floor**: Ground, 1st, 3rd floors + Penthouse
- **Type**: Combined TAB report + reduced-scale duct/piping plans (75 pages)
- **Summary**: Fan/coil/VAV TAB data plus M20.0-M20.2 piping, M10.0/10.2/10.4 ductwork, and color-coded "CBA Level G/1/3 Air Flow Plan" pressure-cascade diagrams. Fine print not legible at rendered resolution.

### B74/B74 HVAC Zone Level 1/3rev/G.pdf
- **Area/Floor**: Level 1, Level 3, Level G
- **Type**: HVAC temperature-control zone plans
- **Summary**: JAX Facilities Engineering (drawn by PCT), dated 9/13/2018. Level 1: VAV-6,7,8,9,10,13,35, RD-2. Level 3: VAV-5,11,12,37, RD-4. Level G: VAV-1,3,4, RD-1 (near loading dock/electrical). These directly correspond to the BAS zone naming in "Point Naming.pdf" below.

### B74/JAX B74 As Built REV1.pdf
- **Area/Floor**: All levels — content only partially verified (146 pages, ~48.7MB, garbled OCR text)
- **Type**: Multi-discipline as-built binder, Project 25016, dated 7/20/2018
- **Summary**: Per bookmark index: RF Shielding Room (MRI room) as-built, Fire Protection, Mechanical & Plumbing (AHU-1/2, EAHU-2, VAV boxes, unit heaters), Ductwork as-built (same penthouse/floor plans found individually below), HVAC I&C as-built (JCI BAS control-point schedules, NAE-32, contract 6N63-0154), Electrical + panel schedules, Site Utility, Master Utility Upgrade. Body-page dimensions/CFM not reliably readable in this pass.

### B74/Jackson Labs Pod 3 T&B Report.pdf
- **Area/Floor**: Pod 3 expansion, penthouse mechanical equipment
- **Type**: NEBB-certified TAB report (36 pages), Tekon-Technical Consultants, dated Sept 25 2018
- **Summary**: SAHU-A/B (York YCO-11x74, ~11,066 CFM design each) and EAHU-A/B (York YCO-108x74); VAV-F/G/H/I/M; reheat/relief diffusers RD-A through RD-H (rooms 74-3xxx/74-1xxx/74-G0xx); HWP-A/B pumps (~230 GPM), CHWP-1/2. References Harriman Project 15434 drawing sheets M10.1A/M10.2A/M10.4A/M10.5A/M10.6A/M20.1A/M20.2A/M20.4A.

### B74/M10-7A through M10-7F (Penthouse Duct Supply Plans 1-6)
- **Summary**: E.P.S. for JCBA, dated 7/4/2017 (Revit JCBA_Duct_All.rvt). Supply ductwork around AHU-1/EAHU-1 and AHU-2/EAHU-2, branches to VAV-1/3/4/5/9/10/12/13/14/35/37, HEPA-6/7, HWC-3/4, HUM-3/4/8. Duct up to 27"x120" down to 6" round.

### B74/M10-8A, M10-8C, M10-8D, M10-8E (Penthouse Duct Exhaust Plans 1, 3, 4, 5 — note: no "8B" or "8F" file present in this folder)
- **Summary**: Same E.P.S./JCBA series. Exhaust ductwork serving VAV-15/16/20/22/23/28/29/30/32, fire/smoke dampers, duct 24"x88" down to 6"-7" round.

### B74/M10.0, M10.2, M10.4 (Ground/1st/3rd Floor Ductwork)
- **Summary**: Full-floor duct plans with extensive red field-markup annotations; small text/duct sizes largely illegible at reviewed resolution.

### B74/POD 3/62_M10-1A, 62_M10-2A, 62_M10-3A, 62_M31-1A
- **Area/Floor**: Pod 3 addition — 3rd floor, 3rd floor interstitial, penthouse, sections
- **Summary**: Harriman, Project 15434, "Preliminary — Not for Construction," Feb 13 2018. M10-1A: balance keynotes (80/60 CFM, 40 CFM), PIV rack connections, 10x10/16x16 drops (marked-up TAB field copy also present). M10-2A: interstitial ductwork 6" round to 18x18, iris dampers at PIV branches (TAB field copy present). M10-3A: four Pod 3 penthouse AHU footprints (SAHU-A/B, EAHU-A/B) with VFDs. M31-1A: sections showing VAV-F/G/H/I/M, HEPA-A through E, HUM-A through E, HWC-A through D, RD-A through H stacked through the section.

### B74/Point Naming.pdf
- **Area/Floor**: Ground/1st/3rd floors (BAS point mapping)
- **Type**: JCI "RS-1 Room Schedule," Contract 6N63-0154, printed 2/13/2017
- **Summary**: Documents the BAS point-naming/zoning convention — each VAV/RD box tied to a room list (74-G010 through 74-3095), controller drawing number, and BAS zone label ("GRD ZONE-1" through "3RD ZONE-21"). Confirms the zone naming used on the B74 HVAC Zone Level G/1/3 drawings above. NC/NAE address and device-address columns are blank in this template.

## Top-level / non-PDF files

### ELS_JAX _ALL_ALL - Penthouse Retrofit 2023-06-27.nwd
- **Summary**: Navisworks 3D BIM federated model (~28.8MB), last modified 2025-03-24 — cannot be opened by the Read tool. "Penthouse Retrofit" scope/building not confirmed; likely a coordination/clash-detection model for a penthouse project (building not confirmed from filename alone).

### duct work main lab penthouse.pdf
- **Summary**: Single-page, untitled 3D isometric BIM screenshot of a mechanical penthouse (color-coded MEP systems). No title block, drawing number, date, or building identification — filename is the only clue ("main lab" penthouse).
