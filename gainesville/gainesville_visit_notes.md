# Gainesville (Momentum Labs) -- Visit Notes & Open Items
**Visit Dates:** July 20-22, 2026
**Prepared by:** Zaal Panthaki, The Jackson Laboratory

---

## Background -- Pre-Visit Humidity Escalation

**February 27, 2026 -- Ken Hovey BAS humidifier changes (winter fix):** Ken made two changes to address winter low-humidity problem: (1) Added humidity transmitter to supply duct "approximately 2/3rds of the way down, mounted outside of Lab 2 in the hallway." (2) Changed humidifier operation from lead/lag to **forced parallel**: "I have forced the two humidifiers to work at the same time at all times and reduced the minimum setpoint to 40%." Ken noted: "A program change to make this normal operation is recommended" -- the parallel override was written values, NOT a permanent BAS program change. This permanent fix was never completed.

**June 1-3, 2026 -- Flush cycle transient issue raised by Kuchta:** Dave Kuchta raised a new open problem: "The system will be running along fine, and then we will see the humidity valve go to 100% and despite this, humidity goes low and into alarm. Then, after a while, humidity rises very fast and the system starts to hunt for a few hours until it stabilizes." Kuchta's diagnosis: humidifier flush cycles -- when humidifier goes into flush/drain cycle, the BAS continues trying to maintain humidity by opening valve to 100%, causing wild transients. Kuchta asked: "Can we get together and talk about this with Ken and some of our controls guys?" Sonia replied to Dave Jun 3 5:54 PM: "Ken stated that he needs to research the humidifiers' flush cycle before getting back to us with an answer. Once he does, I'll arrange for him and Conner to [meet with the team]." Ken never followed up with his research, Sonia never set up the meeting, and the flush cycle issue went unresolved before the summer crisis began. This meeting was never scheduled (flush cycle BAS integration later became the Jul-Aug 2026 follow-up item).

**May 29, 2026 -- Alarm priority relabeling requested (root cause of Jul 20 failure):** Sonia emailed Conner requesting higher BAS alarm priority numbers for 10 categories: CO2, RTUs, PIVs, Cage Racks, Holding Rooms, Procedure Rooms, Necropsy Rooms, Roof Hatch, both boilers operating simultaneously, lights on/off outside 6am-6pm. This work was never completed.

**Jun 8 -- GF3 alarm as Priority 255:** Over the weekend, GF3 temperature alarmed and PIV rack alarmed. BAS displayed both as **Priority 255** (lowest priority). Guard only emailed Sonia -- no urgent response. WiCom cage racks recorded **79 degrees**. Jesse emailed Sonia/Conner: "These alarms should have been Priority 32 for room temp and Priority 22 for PIV rack. We need this system restored." This is a concrete incident proving alarm priorities were misconfigured.

**June 9, 2026 -- BAS server access restored (Epic IT):** Epic IT Solutions (building IT vendor) resolved a BAS server accessibility issue -- server had been unreachable for an unknown period. Dave Kuchta replied to Sonia: "We are back in business with being able to access the server. Now we need to get WW Gay to deal with the alarm priority issues." Alarm priority issues were flagged June 9 but never resolved before the visit. Epic IT contact: Matthew Poteet (IT Technician, 352-240-1281 ext 103, help@epic-it.com).

**June 15, 2026 -- Barrier humidity Critical Event Notice (precursor event):** During a sudden downpour at 13:14, humidity spiked to 94% RH across all 2nd floor barrier spaces simultaneously. System recovered within ~16 minutes. Jesse filed Critical Event Notice at 4:57 PM: "Other raining events haven't had this response in the past." Also: roof leak over lab supply and Lab 2 -- at least one ceiling tile damaged. Responding agency: Concepts + WWG.

Dave Kuchta forwarded the Critical Event Notice to Zaal (CC: Wayne Cameron) at 8:38 PM: "I'd like you to pull the trends and show them to me. I'm curious if you think this is a tuning issue, a system capacity limitation, alarming strategy or something else."

**June 17, 2026 -- Zaal's first RTU trend analysis** (sent to Kuchta/Wayne Cameron, RE: Critical Event Notice):

- **Root cause -- CAPACITY:** OA humidity was 95-100% RH overnight into June 15. Storm hit ~1pm (92°F, humidity spiking). Both RTU-2 and RTU-3 dropped preheat modulation: RTU-2 dropped to **near zero**, RTU-3 dropped to ~12%. RTU-3 supply air humidity spiked to 88% RH during the event, pushing near-saturated air directly into barrier spaces. All barrier rooms spiked simultaneously.

- **Secondary issue -- TUNING:** "Discharge air temps across the barrier SAVs are oscillating +/- 10°F or more under normal conditions. This is not storm-related and likely slowed recovery time. This needs to be addressed separately."

- **Trend data gap:** "Trend logging stopped on June 15, coinciding with the alarm priority update done that day." Resolved the morning of June 17.

- **Zaal's recommendations:** (1) Add BoxFlow trending for barrier SAVs -- not currently logged, needed for future diagnostics. (2) WWG to assess RTU dehumidification capacity given June 15 outdoor conditions and retune discharge air temp control across barrier corridor.

Note: RTU-2 preheat dropping to near zero on June 15 -- same Rht_Modulation behavior Conner confirmed Aug 6 -- indicates both RTUs have the preheat valve capacity/tuning issue, not just RTU-3.

**June 23, 2026 -- Supply DP event (origin of weekly review mandate):** Jesse Hinkle reported "air supply loss and recovery" in the morning. Jesse sent screenshots to Sonia/Stockman. Dave Kuchta forwarded to Zaal + Wayne Cameron: "Sooner or later we're going to have a disaster down there. It is critical that Zaal reviews trends and alarms weekly in detail." Zaal replied: "10-4 will look at this first thing in the morning and get it sorted out." Dave: "Great." -- THIS is the event that created Zaal's mandatory weekly BAS review.

Jesse also reported in the same thread: "`supplydmprcmdint` trend missing -- LAB 1 has had no data since Feb 2025, Holding Room 3 quit reporting in Dec 2024." These are among the 465 non-reporting trend points. Sonia's follow-up email confirmed: **Ken (WWG) had suggested checking Power Meter Data for a voltage spike or dip** -- per his email titled "RTU-3 Static." Ken also said he'd look at the missing trends the following morning. Room Temp and Humidity trends were still populating (not all data was lost). This is the confirmed origin of the open item to check the power meter (192.168.15.57) for Jun 23 voltage anomalies.

**June 24-25, 2026 -- Full trend audit initiated and completed:** Immediately after Kuchta's Jun 23 mandate, Zaal began auditing all ~800 JAX_2nd_Floor history points in Niagara. Jun 24 Zaal emailed Ken Hovey with the first three confirmed missing points for SAV 3-27 Rm 240 Lab 1: `SupplyDmprCmdint`, `RetDamperPos`, `RmPressure_Out`. Ken had replied to Sonia: "I have taken a look at a couple of trends and they appear to be up to date. Are there specific trends not populating?" Zaal provided the list directly.

Zaal completed the full audit Jun 25 8:22 AM and sent results to Wayne Cameron with attachment `gainesville_trend_audit.xlsx`. Summary of ~800 JAX_2nd_Floor history points:

- **SAT boxes (4-x series):** Most have standard trends (RoomTemp, RoomHumidity, DamperCmd/Pos, DischargeAirTemp). Missing: SAT 4-2 EffFlowSpt, SAT 4-23 ReheatVlvPos.
- **SAV boxes (3-x series) -- consistently trended:** RoomTemp, RoomHumidity, DischargeTemp, ExhaustDamperPos, ReheatPosCmd, RmPressure_Out, SADamperPOS, DA_Eff_Spt.
- **SAV boxes -- consistently NOT trended:** BoxFlow, RHTVLV_POS, RetDamperPos, RoomTempint, SupplyDmprCmdint, expectedRet_CFM.
- **Notable exceptions:**
  - SAV 3-2, 3-4, 3-5: No trends on ANY points
  - SAV 3-13, 3-14: No RmPressure_Out trend (present on all others)
  - SAV 3-27A, 3-30A: Only SADamperPOS has a trend -- all other points missing
  - SAV 3-34: Significant gaps -- only RmPressure_Out, RoomHumidity, RoomTemp, SADamperPOS; DischargeTemp, ExhaustDamperPos, ReheatPosCmd missing
  - SAFlowSpt, ExhVlvFlow, TotalFlow, cfg0/cfg1: Not trended across all boxes
  - LabExhaust (2-fan and 3-fan) and OptimizerSupervisor: No trends

Zaal's recommendation: Review whether trends should be added for SAV 3-2, 3-4, 3-5 and the "A" suffix boxes (3-27A, 3-30A), as those have essentially no data being captured. Dave Kuchta replied Jun 24: "Excellent. I look forward to seeing the list."

**June 25, 2026 -- Conner pressure sensor PM (disregard all pressure alarms):** Sonia emailed Jesse, Zaal, and Stockman at 10:28 AM: "Conner from WWG-Controls is currently onsite working on the pressure sensors. Please disregard all pressure alarms until further notice." This is the same day Zaal completed the full trend audit (Jun 25 8:22 AM). Conner being on-site Jun 25 aligns with the trend audit -- if any pressure-related points showed anomalies during that window, the cause is PM work, not a system fault.

**June 29 -- GF3 Holding Rm 3 temperature escalation:** Jesse sent 4-month trend data to Sonia/WWG/Kuchta showing spikes worsening:
| Month | High | Low |
|-------|------|-----|
| March | 69.2 | 67.8 |
| April | 70.2 | 67.8 |
| May | 72.6 | 66.9 |
| June | **76.2** | **65.5** |
"This needs to be investigated and resolved." Sonia asked WWG: "Are our boilers causing this?" (Red Category email)

**July 7-8 -- GF3 temperature spikes (pre-humidity):** Jesse Hinkle reported to Stockman/Sonia/Zaal/Kuchta: "temperature spike in GF3 at 71.9" (Jul 7) and "at 72.4" (Jul 8). Jesse also noted: "We also had what should have been an alarm, but wasn't showing up on the BAS alarm screen." Stockman replied "Yes we are on it." -- BAS alarm screen failure was already a known issue on Jul 8, weeks before the visit.

**July 12-13 storm event** -- initial humidity alarm cascade across multiple rooms. Proc Rm 4 has been running at 80-95% RH since approximately July 12.

**July 16** -- Sonia emails WWG: "The humidity alarms have been going off all day today." She is manually acknowledging alarms every 15-30 minutes and noting they reappear. Outside humidity is ~55%, so this is an indoor problem.

**Conner's July 16 key statement** (in reply to Sonia): "The humidity is essentially locked in as the air handler and the phoenix valves do not have a dehumidification mode. If JAX is open to another program addition that would allow the animal rooms to go below 69 degrees towards the 66 -- 65 degree range to allow dehumidification." Proposed lowering room temp setpoints from 69°F to 65-66°F as the dehumidification path. (This proposal was sent to Sonia/Mark/Ken -- not yet clear if JAX approved or responded.)

**July 19 -- Saturday overnight event** -- humidity climbed across multiple rooms overnight. Root cause (at the time): RTU-3 reheat valve stuck at 0, meaning no reheat = no dehumidification. Same underlying issue as Proc Rm 4. This event triggered the July 20-22 site visit.

**July 20 10:58 AM -- Rm 240A (Lab Supply) humidity alarm (visit day):** Sonia emailed Zaal (only): "Conner mentioned that this is one of the rooms affected by indoor humidity from the storm that came through 2 weekends ago. However, can you check the room to see if there is anything visible affecting its humidity levels?" Conner attributed the Lab Supply humidity to storm carryover from approximately Jul 4-5 weekend. Sonia asking Zaal to physically verify room conditions. This was the first task Sonia sent Zaal on arrival day, before the Proc Rm 4 alarm screen failure was discovered.

**July 20 10:11 AM** -- Last BAS humidity alarm from Proc Rm 4 that reached Sonia's front desk screen. After this, the front desk BAS alarm screen stopped receiving Proc Rm 4 alerts -- humidity climbed from 71% to 89% (Jul 21 morning) to 94% (Jul 21 evening) with no alarms. Jesse Hinkle detected the problem via a handheld humidity reader, not BAS.

---

## Key Contacts

- Conner Townsend (WWG Gay Controls) -- ctownsend@wwgmc.com, 352-681-2389 -- BAS SME
- Ken Hovey (WWG Gay Controls) -- controls engineer
- Mark Garcia (WWG Gay Controls) -- MGarcia@wwgmc.com -- Controls Service Manager
- Negheen Zaman (WWG Gay) -- nzaman@wwgmc.com, 352-264-2612 / 352-756-2721 -- Project Manager, service coordination
- Sonia Hopewell (Concept Companies) -- shopewell@conceptcompanies.net, 646-645-9855 (cell) -- site coordinator
- David Stockman (Concept Companies) -- dstockman@conceptcompanies.net, 352-895-8853 -- contact when Sonia OOO
- Jonathan Jury (Concept Companies) -- jjury@conceptcompanies.net
- Luke Smith (Concept Companies) -- luke@conceptcompanies.net
- Jesse Hinkle (JAX Gainesville) -- jesse.hinkle@jax.org, 352-284-3465 -- Operations Manager
- Dave Kuchta (JAX) -- budget approvals, JACE quote
- Mike Fort (WH Construction) -- Mike@whconstructionfl.com -- refrigerant leak / compressor work
- Ashton (WH Construction) -- ashton@whconstructionfl.com -- compressor inspection/reset (Jul 28 on-site)
- Kevin (WH Construction) -- Aug 6-7 lead technician for refrigerant leak repair; found t-pipe crack
- Shelton (WH Construction) -- Aug 5 on-site technician; diagnosed RTU at 80% capacity after vestibule valve restart
- Ryan Weimar -- ryanw.rmw@gmail.com -- CC'd on RTU-3 thread, role unknown
- Wade (Nelson & Company) -- field technician for RTU work
- Rory Stiglitz (Nelson & Company) -- rep who submitted Pure Humidifier submittal
- Newton Freire -- provided Pure Humidifier submittal PDF
- Andy Fernandez (EPIC IT) -- power meter
- Brandon Shakespeare -- WiCom networking
- Amanda Dowtin (JAX) -- cell bio room
- Wayne Cameron (JAX) -- Wayne.Cameron@jax.org -- peer to Zaal, also monitors Gainesville BAS remotely
- Ashley Beaton (JAX PQC) -- Ashley.Beaton@jax.org -- qualifications team, handles rack certifications
- Kyle Martin (JAX) -- Kyle.Martin@jax.org -- on multiple Gainesville threads
- Karine Lux (JAX) -- Karine.Lux@jax.org -- on WiCom/networking threads
- Sabrina Rosario (JAX Gainesville) -- Sabrina.Rosario@jax.org -- Jesse's on-site tech
- Brian Crawford (Concept Companies) -- brian@conceptcompanies.net
- Hank Pate (Concept Companies, FORMER) -- hpate@conceptcompanies.net -- **Left Concept Companies April 28, 2026.** Was tracking flush cycle concerns Feb-Apr 2026 alongside Kuchta. No longer reachable. Facility management concerns passed to Stockman/Jury/Luke Smith.
- Eric Rossow (JAX) -- Eric.Rossow@jax.org -- on WiCom threads
- Dave Kuchta (JAX Bar Harbor) -- David.Kuchta@jax.org, 207-288-6182 -- senior stakeholder, budget approvals

---

## RTU-3 / Humidity -- Priority Item

**What happened:**
- RTU-3 reheat valve behaving erratically, randomly sticking and hunting
- Caused Procedure Room 4 (SAV 3-17) to run at 80-95% RH since approximately July 12
- Wider pattern: multiple rooms showing humidity alarms (Proc 5, Surgery, Behavioral, Clean Storage, Cell Bio, others)
- Saturday July 19 overnight spike was the direct trigger for this visit

**RTU-3 Control Architecture (two layers):**
- **Layer 1 (Honeywell/BAS):** Run/start command, percentage commands to humidifiers, general setpoints -- this is the Honeywell side that Conner/WWG manage
- **Layer 2 (AnnexAir local communication):** Handles actual compressor staging independently of Honeywell. When compressor VFDs trip to alarm, AnnexAir local comm shows "all compressors commanded to run" but pressures equalized = circuits not actually running. Compressor banks are numbered 2, 3, 4 in AnnexAir comm. (Source: Mark Garcia July 25 service report)
- Implication: BAS may show compressors commanded on while physically they are faulted/off. The BAS layer and the AnnexAir local layer can be out of sync.

**Zaal's Jul 22 site visit recap email** (to Sonia/Kuchta/Stockman/Wayne/Jesse, CC: Ashley Beaton):
Top 10 items in priority order:
1. RTU-3 reheat valve erratic -- rooms at 80-95% RH since Jul 12. Root cause: "faulty control board on RTU-3 causing the reheat valve to randomly stick and hunt." Nelson & Company must diagnose.
2. Humidity alarms in Proc 4, Proc 5, Surgery, Behavioral, Clean Storage, Cell Bio -- all tied to RTU-3.
3. 879 trend points audited, 465 not reporting. Doing second pass, fixing directly on server.
4. Flush cycles causing overnight false alarms. Real fix = BMS integration so valve does not go to 100% during flush. Following up with Conner.
5. JACE offline notifications -- $737.28 quote attached. Waiting approval.
6. SAV 3-2, 3-4, 3-5 -- trends configured but never received data. Asked Conner to add them.
7. Rack work in GF3 -- 2 new racks installed, 4 recertified. Ashley Beaton has certs.
8. Air valve cell bio room -- parts being ordered (Amanda Dowtin coordinating).
9. Dimmer in animal room -- fixed.
10. Microbiological filter -- taken care of.
"In Progress": second pass trend audit; JACE approval; **BAS documentation for Jesse/team/management**; flush cycle conversation with Conner.

**July 23 -- Sonia's TOP PRIORITY escalation:** Sonia emailed Negheen Zaman (WWG PM) with subject "TOP PRIORITY: RTU-3 Control Board Causing High Humidity in Room(s)." Based on findings from Zaal and Conner's trend analysis: "Procedure Room 4 (**SAV 3-17**) has been running at 80-95% relative humidity since approximately July 12." Root cause attributed as: "faulty control board on RTU-3 causing the reheat valve to randomly stick and hunt." Sonia asked: (1) Who at WWGay is contacting Nelson and Co. to dispatch a tech? (2) Quickest available dates for control board repair (Jesse needs to confirm timing with his team). (3) Is the control board under warranty? -- This email established that SAV 3-17 = Procedure Room 4, which is confirmed as the primary affected barrier space.

**Conner's Jul 23 correction**: "Just a correction -- the board may not be bad. A Nelson & Co rep just needs to hook up to the RTU's factory controls and see what is going on with the reheat valve program."

**Zaal's Jul 27 three-item follow-up** (to Conner/Sonia/Negheen, CC: Jesse/Mark/Kuchta/Wayne): (1) Status on JACE offline notification quote? (2) Is there a way to suppress humidity alarms during humidifier flush cycles so we are not getting false alarms overnight? (3) Do you have any documentation or a guide for the WWG Gay server we could reference?

**Conner's Jul 27 three-item reply**: (1) JACE quote -- Mark Garcia will send. (2) Flush cycles: "As far as I'm aware, we are not monitoring the humidifiers. We only tell them to start, and then give them a percentage command when needed. If it's possible to monitor the flush cycle of the humidifiers, I am not sure." (3) Training: "We can provide a training day for you or whomever else JAX would like to run through the front end operation."

**Kuchta's Jul 27 private reply to Zaal** (sent only to Zaal + Wayne Cameron, NOT to the full group): Kuchta replied at 11:43 AM with his engineering vision for the fix. "On the humidifier flush, there is a little more to it than simply suppressing the alarms. In an ideal world, we would integrate it with the BMS so that when there is no steam for humidity during the flush cycle, the humidifier control valve does not go to 100% and keep trying to add steam when there isn't any. Then instead of going into a hysteresis oscillation trying to overcompensate, have the system take a more orderly approach regaining control. Then instead of chasing humidity up and down for hours, it could recover more quickly without the wild swings. Finally, during this sequence of events, not throw spurious alarms." This is the requirement that Zaal's Jul 28 Register 202 proposal directly addresses. Kuchta kept this off the main thread -- it was private guidance to Zaal, not a vendor directive.

**Zaal's Jul 28 flush cycle analysis** (to Conner/Sonia/Negheen, CC: Jesse/Mark/Stockman/Kuchta/Wayne):
After reviewing trend data: "The July 11 flush event is the clearest example -- Rht_Modulation dropped from 25% to 1.6% in one 30-minute window and recovered fully in the next. That lines up almost exactly with the 26-minute drain duration spec for the ES-102. So the flush cycle behavior itself is working as designed. The issue is that everything after July 12 is the RTU-3 reheat failure on top of it."
Proposed BAS fix: Modbus Register 202 = Operation Mode (1=normal, 2=draining). ProtoAir gateway can expose to BAS. "When BAS sees Register 202 = 2 on either humidifier, hold the humidifier command steady instead of continuing to integrate up. That would prevent the overshoot when steam comes back after the drain."

**CORRECTION (Aug 6, Conner):** Rht_Modulation is NOT the humidifier valve. It is the **preheat 3-way valve** -- controls hot water flow from boiler piping to the RTU to maintain 55 degree supply air. The Jul 11 drop (25% to 1.6% in 30 min) was the preheat valve dropping, not a flush cycle event. Real open question: what is causing the preheat valve to drop suddenly and force downstream SAV zone reheats to increase? This is likely a controls/tuning issue with the RTU preheat loop. Humidifiers only run in winter, so flush cycles are not currently active. Flush cycle monitoring (Register 202 via ProtoAir gateway) is still a valid winter-prep item but needs a WWG quote as an addition to the BAS network chain (outside original design).

**Jesse's Jul 28 9:13 AM escalation email** (on TOP PRIORITY thread): "I am looking for an update on getting a Nelson & Co rep out to hook up to the RTU's factory controls and see what is going on, per Conner's email. When can we expect them to be out. This is very important as the humidity issue over the weekend proves. If the RTU will need to be shut down, we will need to plan that out with the PCS team." -- Jesse is pushing for answers on the NCJax dispatch timeline and flagging PCS (Preclinical Services) involvement if a shutdown is required.

**Sonia's Jul 28 10:11 AM reply** (Red Category, on TOP PRIORITY thread): Dave Stockman reached Negheen. Sonia called NCJax and is scheduling an urgent visit for RTU-3's control board. She asked NCJax whether a shutdown is required; if so, she requested multiple date options for Jesse and his team to choose from. **Contact: Casey at NCJax** (last name unknown) -- will call back with answers and dates. Negheen also told Stockman that the air valve is still in transit, confirming why the elevator vestibule alarm is continuously firing: "This broken valve is causing the 'Elevator Vestibule' alarm to go off."

**Sonia's Jul 28 10:15 AM update** (flagged, same thread -- 4 minutes later): "NCJax can stop by tomorrow afternoon without needing to take the unit down. I booked it." -- Casey called back. This is the definitive booking confirmation for the Jul 29 Wade Godwin visit. No shutdown required; NCJax can work on the live unit.

**Official Critical Event Notice (filed 5:52 PM Jul 28 by Jesse Hinkle):**
- Incident start: 2026-07-28 at **1:30 PM** (humidity alarm active since 1:30, roughly 3 hours before Conner's 4:31 PM remote alert)
- Incident type: Equipment Failure
- Description: "RTU 3 compressors **and RTU 1 compressors** are not working properly and need to be reset. WH Construction is on their way in to reset the compressors. The humidity in the mouse rooms and other barrier rooms is extremely high and in alarm since 1:30 today."
- Response description: "RTU is not able to handle the humidity and temperature and is down compressors **again**. WH construction is coming in to reset the compressors **again like WWG did over the weekend**. WWG Gay and NCJAX (Nelson and Co) are coming in at 12 [noon next day] to check the compressors and the control board. RTU 1 is having a similar issue so they are going to check all of the RTUs while they are here 1-4."
- Result: mice outside of desired humidity. Status at submission: not resolved yet.
- **RTU 1 was also affected** -- this is broader than just RTU-3. Both units had compressor issues Jul 28.

**Updated root cause (July 28):**
- Conner identified 3 of 5 compressors offline on RTU-3, supply air temperature near 67°F
- With 60% cooling capacity lost, the AHU cannot cool air below dewpoint -- the AnnexAir factory sequence correctly suppresses reheat when SAT cannot reach setpoint
- The "reheat valve hunting" observed in BAS is likely the unit staging remaining 2 compressors on/off trying to chase SAT setpoint, not a primary valve fault
- Overnight Rht recovery (15-22% when OA=100%) confirms valve moves -- lower nighttime enthalpy allows 2 compressors to partially meet load

**July 28 evening (pre-visit action):**
- Conner (4:31 PM, remote) alerted Sonia: 3 of 5 compressors off, supply air 67°F -- recommended calling Nelson & Co. or HVAC service
- Sonia arranged Ashton (WH Construction) to visit that evening; Ashton arrived 5:50 PM and **activated one compressor** -- greatly improved humidity/temps
- Sonia arranged Conner for next morning and Wade for afternoon July 29 (NCJax booking via Casey -- confirmed Jul 28 10:15 AM, no shutdown needed)

**July 29 -- Both Conner and Wade on-site:**
- **Conner Townsend (WWG Gay) -- morning** -- BAS controls review, also on-site with Wade
- **Wade Godwin (Nelson & Company / NCJax) -- afternoon** -- inspected all 4 RTUs with Field Assistant 10 diagnostic tool
- Report filed: "(07-29-2026) ML RTU-3 (STM2607-2554) NC Jax.pdf" -- Job Report #STM2607-2554, July 30, 2026. Authorized by Sonia Hopewell. Customer entity: **Alachua Bio Investments** (property owner), 1449 SW 74th Dr Suite 200, Gainesville FL 32607.
- Wade confirmed to Sonia: reheat valve is controlled by WWG-Controls (not the OEM)
- Warranty parts ordered
- Jesse's Jul 29 4:20 PM update to Critical Events list: "Issues found with **each unit 1-4**. There will be a comprehensive report from NCJAX. RTU-3 has a compressor not working that will require work. Many items needed to be reset." After resets: system restored, BAS all green (except elevator vestibule valve alarm cycling).
- **Elena GonzaloGil's Jul 29 reply (to Jesse + CriticalEventsGainesville + Zoe Hsi + Zaal):** "Thanks so much for the update. Keep us posted on timelines once you receive the report/talk to Concept. I would expect Concept will take this as a high priority." -- Brief acknowledgment from the Associate Director of Preclinical Services. No action items, but confirms senior research leadership is watching the thread.

**NCJAX Report -- RTU-by-RTU Findings (Wade Godwin, July 29, 2026):**

- **RTU-1:** Down unit -- tripped on circuit B low pressure on **July 7, 2026**. Wade reset; powered into unit, all circuits came back up, maintaining supply air. Wade note: "May need further service in case of reheat valve is getting stuck -- could not see that today." RTU-1 reheat valve suspected but unconfirmed.

- **RTU-2:** Found compressor **drives 4 and 5 tripped**. Reset. Hooked up Field Assistant 10 -- no alarms, unit maintaining supply/return temperatures.

- **RTU-3:** Hooked up Field Assistant 10. Found compressors 4 and 5 in alarm. Reset compressor 4 (came back). **Compressor 5 = permanent alarm -- zero refrigerant (0 PSI) in circuit 5.** Wade: "Circuit 5 needs a leak check. Wall around lines in the back of the compressor." This is the confirmed refrigerant leak requiring the Aug 6-7 WHC leak search. **Conner (Aug 6 PM) additional update:** Circuit 5 is "completely flat" and circuits 3 and 4 "keep having intermittent issues" -- more circuits affected than the July 29 report indicated.

- **RTU-4:** Found compressor 1 drive in alarm. Reset; drive came back. Second stage came in later, maintaining supply temperature. No other problems found.

**Parts/warranty:**
- Wade Godwin from Nelson & Company confirmed parts are under warranty -- ordering underway
- Warranty expiration date not yet documented -- request from Nelson & Company
- No commissioning or startup report located in email history

**July 30 -- Sonia's distribution of the NCJAX report** (to Stockman/Luke/Jonathan Jury, CC: Jesse/Zaal):
- Attached the NCJAX report PDF
- Noted: "I'm working on setting dates for next week to test RTU-3 and locate the unit's refrigerant leak. Also, the elevator vestibule air valve will be replaced next week."
- This establishes the Aug 4 vestibule valve replacement and refrigerant leak work were both planned as of July 30.

**Elevator Vestibule Air Valve:**
- As of July 28, Negheen confirmed to David Stockman that the valve was still in transit / on order. The broken valve was actively triggering the "Elevator Vestibule" alarm.
- **August 4 confirmed** -- Negheen Zaman (WWG PM) confirmed "We will see you Tuesday morning" to Sonia's July 31 scheduling email
- **COMPLETED August 4** -- Sonia's Aug 5 email explicitly references "yesterday's shutdown of RTU-3 for the replacement of the Elev Vest Air Valve." Valve is installed.
- August 4 contact was Stockman (Sonia was OOO). Jonathan Jury (Concept Companies) showed WWG the valve location.
- RTU-3 shutdown scheduled for approximately 1 hour during the work
- Question still open: does Conner need to reprogram or reboot BAS after replacement? (asked in Sonia's email, no answer yet)
- David Stockman is the Concept Companies point of contact that day (Sonia was OOO)
- **Aug 4 WiCom alarms during RTU restart:** Jesse replied to WiCom blower alarm notifications (GNV02-BL01, GNV02-BL07) at 1:26 PM and 2:31 PM. 1:26 PM: "We had RTU work being performed today. RTU has been off, but is back on. We should see things start to stabilize." 2:31 PM: "WWGAY got the compressors running. Room temps and humidities are starting to stabilize." -- Confirms WWG (Conner) had to re-engage the compressors remotely after the Aug 4 RTU restart. This is the direct precursor to the Aug 5 morning humidity alarm wave: compressors were struggling from the moment of the Aug 4 restart.
- No completion confirmation email for the valve work itself -- assumed done given confirmed Aug 4 visit

**August 5 -- Post-Restart Humidity Alarms (after Aug 4 vestibule valve shutdown):**
- Sonia's Aug 5 11:27 AM (to Jesse + Zaal, CC: Stockman/Luke): "There have been humidity alarms going off all morning. I notified Conner of WWG-Controls. It wasn't happening this past Monday. So, I'm attributing the issue to yesterday's shutdown of RTU-3 (for the replacement of the Elev Vest Air Valve). I asked him if any of the compressors need to be reset. Conner is currently looking into the issue remotely." Includes an attached screenshot (image.png, 239KB, presumably a humidity alarm dashboard or BAS trend).
- **Conner's Aug 5 remote view (before Shelton arrived)**: Compressors 1, 2, and 4 are working. Compressor 3 is working intermittently. (Compressor 5 completely down.) This matches the Aug 5 compressor status.
- Jesse Aug 5 1:55 PM (to Sonia, CC: Zaal/Stockman/Luke): "Thank you for the update, Sonia. So, if the compressors were working as they should be except for #5, but we were still having these humidity issues today, why is my next question? What is causing us to have these humidity issues?" -- Jesse pressing for root cause.
- Sonia's Aug 5 2:16 PM reply to Jesse relaying Shelton's diagnosis: **"Shelton (WHC) told me that the weather is causing the RTU to show that one of its compressors is actually down. It being down is different from it being on standby. So, the RTU is operating at 80% capacity, not 100%. With one compressor down, the rest of the unit's trying to compensate."** Additionally before Shelton arrived, Conner (remote) confirmed compressors 1, 2, 4 working and 3 intermittent. Shelton also confirmed none needed resetting -- the issue is a dead compressor, not a tripped breaker. Alarms "considerably subsided." **WHC scheduled for tomorrow at 8-8:30 AM to find/repair the leak in compressor 5.**
- Stockman Aug 5 2:45 PM: "WWGAY said one set of compressors stays off at all times and it rotates to a different bank all the time. Maybe we should confirm that." -- Referencing Conner's lead/lag staging explanation. Stockman wondering if this accounts for what they're seeing.
- Sonia's Aug 5 3:01 PM to Stockman: "I'll talk to Conner again, but, wouldn't that explain why compressor #3 is working intermittently?" -- Sonia asking if the AnnexAir lead/lag staging rotation explains compressor 3's intermittent behavior. The real answer is no: compressor 5 has zero refrigerant (confirmed dead), not a lead/lag parked unit, and compressor 3's intermittency is a separate issue. This staging confusion has not been formally clarified to Sonia.

**RTU-3 Refrigerant Leak:**
- **August 6** -- Kevin (WH Construction) arrived 10:30 AM, left 3:30 PM. Kevin and his assistant found a **crack in the "t-pipe"** (possibly caused by unit vibration) with refrigerant splattered on the RTU walls. Kevin returning Aug 7 to finish by 8 AM; he said no problems should occur overnight. After completing the job, Kevin will send a written report detailing findings and repairs. Sonia alerted building security to call her if anything unusual occurs overnight. (Source: Sonia's Aug 6 4:24 PM email "RTU-3 UPDATE: Refrigerant Leak (Find and Repair)")
- RTU-3 does NOT need to be shut down for this work
- Calendar invite originally 8 AM - 12 PM; Sonia updated to 10:30 AM - 3:30 PM reflecting WHC's actual on-site window
- Aug 7 (today): Kevin expected to finish by 8 AM. Written report from Kevin to follow. **Work in progress -- no completion email yet.**

---

## Humidifier Flush Cycles

**Background timeline:**
- **May 13, 2026**: RTU-3 freeze stat installed (CONFIRMED). Ordered Feb 2, 2026; part on-site March 4, 2026; scheduling delays pushed work to May 13. Installed by **Wade Godwin (NCJax)** at 2 PM per work order. Jesse Hinkle provided dates after multiple delays (work set for 4/9/26, then rescheduled 4/22/26, then rescheduled again -- May 13 confirmed May 1). Source: JAX Weekly List 6.17.26.pdf.
- **Before Feb 2026**: Humidifiers were running lead/lag -- caused humidity maintenance issues
- **Fixed pre-visit**: WWG changed humidifiers from lead/lag to **parallel** operation -- resolved general humidity maintenance
- **May 20, 2026 -- Sonia raised seasonal stability question**: After the freeze stat replacement, Sonia asked Ken: "Due to the recently replaced Freeze Stat for RTU-3, we will most likely need to determine if additional fine-tuning is necessary and if humidifiers will remain stable as we transition from season to season." Ken was asked to advise on next steps. This question was never formally answered before the summer humidity crisis began.
- **Jun 2-3, 2026 -- Ken Hovey response to seasonal stability question:** Sonia asked Ken: "Is it possible to download a spreadsheet showing those new adjustments? Will those adjustments be problematic during summer's temperatures? ...meaning, too humid?" Ken replied Jun 2: "I do believe that once we started running the humidifiers in parallel instead of the original configuration of lead/lag we were able to maintain the humidity in the vivarium." On Jun 3 after Sonia's follow-up, Ken's full answer: **"There is not a way to produce a spreadsheet to show the programming. We did go through the program during several meetings while troubleshooting the issue. The humidifiers only engage when the humidity is low in three of the holding rooms, otherwise the natural function of the system design should mitigate high humidity during the summer months."** Key implications: (1) Ken confirmed parallel operation was the fix. (2) Ken's position was that summer high humidity would self-regulate -- this proved incorrect. (3) No programming documentation exists. Sonia forwarded Ken's response to Jesse and the team.
- **Feb-Jun 2026**: Ongoing concern about flush-cycle-induced transients, tracked by Dave Kuchta and Hank Pate (Concept Companies Facilities Manager)
- **Jun 2, 2026**: Ken Hovey confirmed parallel operation resolved general issue; said flush cycle configuration was unknown to him
- **Jul 1, 2026**: Ken confirmed flush can be triggered via external input, runtime, or elapsed time, but did not know current config; proposed triggering flush through BAS to enable trending
- **Jul 16, 2026**: Sonia forwarded full thread to Zaal before site visit

**Issue:** Overnight humidity alarms triggered during humidifier flush cycles. System goes into hysteresis oscillation -- humidifier control valve goes to 100% chasing steam that is not there during the flush, causing wild humidity swings for hours.

**Sonia's Jul 16 summary of the full flush cycle investigation thread (forwarded to Zaal before the visit):**
"David Kuchta from JAX Labs reported that the electric humidifier's flush cycles were causing severe humidity transients and late-night alarms. During a flush cycle, the humidifier shuts down to prevent scale buildup, causing the system to overcompensate by opening the humidity valve to 100%. This results in a sharp drop in humidity, followed by a rapid spike and several hours of stabilization hunting. Controls Software Engineer Ken Hovey initially stated he needed to research the issue. Upon reviewing the documentation, Ken noted that the flush operation can be triggered by an external input, accumulated runtime, or elapsed time, but he was unsure how it was currently configured. To resolve the issue, Ken proposed investigating the requirements for triggering the flush sequence through the Building Automation System (BAS). This integration would allow him to disable commands to the humidifier and actively trend the flush cycle, rather than guessing when it occurs."

**Dave's guidance (received July 27):**
The fix is not just alarm suppression. Needs full BAS integration:
1. During flush cycle, when no steam is available, humidifier control valve should NOT go to 100%
2. Avoid hysteresis oscillation and overcompensation
3. System should take an orderly approach to regaining control
4. Recover quickly without wild swings
5. Only then suppress alarms during the controlled recovery sequence

**Trend analysis -- 30-minute interval data (SAV 3-16 Proc 3, July 1-27):**

July 1-10 is clean baseline: humidity 50-58%, no spikes.

**July 11, 4:30 PM -- clearest flush cycle event in the dataset:**
- 4:00 PM: 51% (normal)
- 4:30 PM: 81% -- 30-point jump in a single 30-minute window
- 5:00 PM: back to 55%

This is the textbook flush + integrator windup pattern. The humidifier went offline during flush, BAS drove valve to 100%, humidifier came back and blasted the room. This happened the day before RTU-3 started degrading, so it is a clean isolated example with no RTU-3 noise on top of it.

**July 12 onwards -- RTU-3 failure layered on top.** The flush cycle pattern is still happening but now sits on an already-elevated baseline of 60-80%. Much harder to separate the two issues. Daily pattern: drops overnight to 56-66%, climbs through business hours, peaks around 10-11 AM.

**Conner's July 15, 6:21 AM analysis (to Sonia, CC: Mark Garcia, Ken Hovey, Stockman, Jesse -- forwarded to Zaal by Sonia same day):**
This is Conner's most detailed structural explanation of why humidity stays elevated. Key text verbatim:
"those rooms may remain at their current humidity, give or take a few % throughout the day. This is because the RTU-3 constantly supplying 55-degree air into the animal rooms, while the SAVs maintain a constant critical setpoint of 69 degrees. All of the rooms are in minimal cooling airflow due to the temperature being at setpoint. This is not allowing enough of that cool air to enter the space to knock the humidity down, as well as the SAVs not having a Dehumidification mode. In short, the RTU and SAVs are blind to the current humidity being too high."

Root cause of the specific July 12 spike: "This was caused when RTU-3 started back up and introduced a bunch of outside air into the spaces before the compressors could cool down the supply air temp to 55-degrees."

**Structural implications:**
- Rooms at 69°F setpoint means SAV dampers are nearly at minimum -- very little cool air entering spaces
- With minimal airflow, humidity in the space is not being turned over and knocked down
- RTU has no humidity feedback loop; SAVs have no dehumidification mode
- System can only dehumidify indirectly by cooling supply air to 55°F and forcing enough airflow through -- but only if rooms are calling for cooling
- **This is the design gap that Zaal's 65-66°F proposal targets**: dropping room temp setpoint forces SAVs to demand more airflow, pulling in more dehumidified supply air

Graph legend (Humidity.png): blue = room temperature, green = humidity, purple/dark blue = leaving coil temperature / supply air temperature on RTU-3 after startup.

**July 25, 12:30-3:00 PM -- extreme event:** Room hit 99-100% RH for 2.5 hours, did not drop below 65% until 9 PM. **Root cause confirmed:** compressor VFDs tripped to alarm state. Mark Garcia (WWG Gay Controls Service Manager) responded after hours, went to roof, reset all compressor VFDs; discharge air normalized from 65-67°F to 56°F at departure. Unit running normally when he left. (Source: "Gene of WWG after hrs call 7/25" forwarded email -- report written by Mark Garcia despite "Gene" in subject.)

**Conner's reply -- Aug 6, 10:12 AM:**
- **Rht_Modulation is NOT humidifier-related.** It is the preheat 3-way valve from the boiler piping to the RTU -- maintains 55°F supply air.
- Flush cycle monitoring "would have to be looked at as an addition to the BAS network chain. This would defer from the original design, so we would need to quote it."
- Humidifiers only run in winter, so flush cycles are not currently active.

**Zaal's reply to Conner -- Aug 6, 2:48 PM (CC: Mark Garcia, David Kuchta, Wayne Cameron, Jesse Hinkle):**
Three specific questions asked (still partially open):
1. Is a sudden drop to near-zero a known behavior -- summer reset logic, economizer interaction, supply air temp override -- or does it point to a controls problem?
2. Are there conditions under which the preheat loop is designed to go to minimum? (Ruling out intentional setback before pursuing repair.)
3. Is there any existing alarm or trend on preheat valve position we should be watching, or is that something to add?
Also asked for a formal quote: "Please put together a quote for adding the humidifier operation mode (Modbus Register 202 on the ProtoAir gateway) to the BAS network as a separate line item."

**Conner's follow-up reply -- Aug 6, 2:59 PM EDT (in response to Zaal's 3-question follow-up):**
- **Root cause of Rht_Modulation drops confirmed: compressor failures.** Conner: "the reheat valve modulates to maintain that 55 degree air, which hasn't been a problem until recent. This is due to the compressors having issues."
- **Circuit 5 is completely flat** (zero PSI, confirmed dead -- consistent with NCJAX report)
- **Circuits 3 and 4 have intermittent issues** -- new information. Previously only circuit 5 was confirmed failed. Conner says "circuit 3 / 4 I believe keep having intermittent issues."
- **Implication:** When compressors fail, supply air temperature rises above 55°F, so the preheat controller has no reason to fire -- drives valve to 0%. The sudden drops are a direct symptom of compressor cycling/failure, NOT a controls programming issue and NOT flush-cycle-related.
- Answered Zaal's Q1 directly. Q2 (intentional setback) and Q3 (preheat valve alarm/trend) NOT yet answered -- still open.
- **Flush cycle quote:** Conner will coordinate with Mark Garcia. "I will let you know what we come up with."

**Mark Garcia (WWG Gay) -- Aug 6, 11:56 AM (RE: TOP PRIORITY thread):**
- Offered on-site training: "Hi Zaal, would you like to schedule training sometime soon? We could just bill per hr. that we are on site with you guys if that would be helpful."
- Response needed: coordinate with Jesse on budget/scheduling before replying.

**WiCom blower mass offline event -- Aug 6, 8:45-9:01 AM:**
- Allentown WiCom system sent simultaneous offline notifications for multiple blowers across all three rooms: GNV01-BL02, GNV02-BL01/BL02/BL03/BL07, GNV03-BL03/BL06.
- All fired within a ~15-minute window, suggesting a network blip or BAS server restart rather than individual blower failures.
- GNV03-BL06 recovered and subsequently reported Exhaust Humidity Alarm multiple times in the afternoon (1:56, 3:43, 4:14, 4:42, 4:53, 5:01 PM) -- consistent with the ongoing RTU-3 dehumidification failure that day.

**Zaal's July 28 deep-dive analysis to Conner (full thread):**
- Humidifier model: **ES-102** (confirmed 26-minute drain duration per spec)
- July 11 event in trend data: Rht_Modulation dropped 25% to 1.6% in one 30-minute window, fully recovered next interval -- exactly matches ES-102 26-min drain spec. Flush cycle mechanics are working as designed.
- Data from July 12 onwards is contaminated by RTU-3 failure. Need clean data post-repair to isolate flush cycle behavior properly.
- **Technical spec for the change order:**
  - Pure Humidifier INTAC Modbus Register 202 = Operation Mode (1 = normal, 2 = draining/flush active)
  - **ProtoAir gateway** (included in the equipment submittal) should already be able to expose Register 202 to the BAS
  - When BAS sees Register 202 = 2 on either humidifier, hold humidifier command steady -- stop integrating up
  - Prevents the integrator windup and overshoot when steam comes back after the drain

**Status:** Flush cycle BAS integration requires a change order quote from WWG Gay. Technical path is clear (ProtoAir exposes Reg 202, BAS holds command on flush detect). No further action until RTU-3 is repaired and we decide if the quote is worth pursuing.

---

## Full Punch List

### Waiting on Someone Else

| Item | Status | Waiting On | Next Step |
|------|--------|-----------|-----------|
| RTU-3 compressor repair | Parts under warranty (Wade Godwin July 29). **Compressor 5 fully down** Aug 5 (Shelton/WHC). Aug 6: Kevin (WHC) found **crack in t-pipe**, refrigerant splattered on RTU walls. Returning Aug 7 to finish by 8 AM; written report to follow. Compressors 1, 2, 4 working; 3 intermittent; 5 dead (zero PSI). | Kevin (WH Construction) completing Aug 7 | Await Kevin's completion + written report |
| RTU-1 through RTU-4 compressor inspection | Wade inspected all 4 RTUs July 29. Report: (07-29-2026) ML RTU-3 (STM2607-2554) NC Jax.pdf | Nelson & Company | Read PDF report for full findings |
| Elevator vestibule air valve replacement | **COMPLETE Aug 4** -- confirmed by Sonia Aug 5 email | WWG Mechanical | Done -- valve replaced during 1-hour RTU-3 shutdown |
| JACE offline notifications | **Stockman confirmed "Yes!" Aug 5 7:27 PM.** Zaal forwarded quote to Kuchta Aug 5; Kuchta pushed to Stockman same day ("work with WW Gay, get us a Work Order"); Stockman replied "Yes!" (CC: Zaal, Sonia). Work Order not yet issued but Stockman has committed. | Monitor for WWG Gay to issue WO |
| SAV 3-2, 3-4, 3-5 trends (first floor) | Conner confirmed Aug 3: SAVs 1-5 always trending -- they are on the **FirstFloor_JACE** history database (separate network/JACE from JAX_2nd_Floor). 3 screenshots sent showing how to access: Histories button > pick FirstFloor_JACE in history picker. | No further action from Conner needed | Switch history picker to FirstFloor_JACE to view SAV 1-5 data |
| Humidifier flush cycle BAS integration | Conner (Aug 6 AM): requires change order quote. Conner (Aug 6 PM): coordinating with Mark Garcia, will advise. Humidifiers winter-only, not urgent. | WWG Gay | Await Conner/Mark quote |
| SAV 3-34 exhaust damper / GF3 ExhaustDMprPos=0% | Jesse (Jul 22, 4:20 PM): Wi-com alarm on one GF3 rack cycling between 73-74°F; BAS shows room at 69.3°F. Jesse observed ExhaustDMprPos = 0% for GF3 SAV -- confirmed always at 0% in trend, observed twice. GF2 exhaust at 54%, GF1 at 65% for comparison. Stockman forwarded to Conner: "high priority -- mice in this room." Conner (Jul 23, 11:08 AM): "Those exhaust dampers on the trends are solely for room pressure management only and do not affect the animal cages. I will look into the exhaust that pulls from those cages and see if there is an issue once I get a chance." | WWG Gay | Follow up -- has Conner looked into cage exhaust? No confirmation received yet. |
| WiCom blower networking | Brandon Shakespeare notified | Brandon Shakespeare | Follow up to confirm complete |
| Commissioning records / AnnexAir startup report | Not found in email history | Nelson & Company / Concept Companies | Request from Wade during July 29 visit |
| WWG BAS training day | Mark Garcia asked Aug 6 if Zaal wants to schedule training -- billing per hour on site | WWG Gay | Respond to Mark -- coordinate with Jesse on budget/scheduling |

### Zaal To-Do

| Item | Status | Notes |
|------|--------|-------|
| Enable 4 trend points (Humidifier_1_Cmd, Humidifier_2_Cmd, SAV 3-16 RHTVLV_POS, SAV 3-17 RHTVLV_POS) | Waiting on Conner | Asked Conner about red arrow / fault state on history extensions Aug 3. Awaiting reply on how to fix. |
| 465 non-reporting trend points | In progress | Will continue after Conner clarifies history enable process. Priority: SAV 3-1, 3-2, 3-4, 3-5, 3-27A, 3-30A. |
| JACE offline notifications quote | **Stockman confirmed Aug 5 7:27 PM** -- Kuchta's "Can you please work with WW Gay and get us a Work Order?" got "Yes!" from Stockman (CC: Zaal, Sonia). Work Order not yet issued. | Follow up if no WO from Stockman/WWG by ~Aug 10 |
| Holding Room 3 exhaust damper | Closed | Conner confirmed behavior is OK. No further action needed. |
| BAS Niagara documentation | Deferred | Will be done as part of a training session with Jesse. |

---

## Completed During Visit

| Item | Notes |
|------|-------|
| Rack work GF3 | 2 new racks installed, 4 recertified, certs 019 and 020 filed in GNV share folder |
| Power meter (192.168.15.57) | Connected, use Firefox with http://, credentials from Bob Terwilliger |
| Air valve cell bio room | Parts being ordered, coordinated with Amanda Dowtin |
| Dimmer animal room | Fixed, resolved with Jesse Hinkle |
| Microbiological filter | Situated |
| SAV 3-29 exhaust damper | Pulled CSV, running at 19% all year, not a concern |
| SAV 3-31 exhaust damper | Still partially open, hitting setpoint, not critical |
| SAV 3-34 exhaust damper | Was a trending issue, situated |

---

## BAS System Notes (Niagara / Vykon)

- Remote desktop access: 192.168.15.235
- Chrome Supervisor URL: https://192.168.15.17/ord/station%7CDrivers/NiagaraNetwork/JAX_2nd_Floor/Alarms%7CsecMM_Alarms
- History/trending is configured at the point level via **NumIntervalExt** (Numeric Interval Extension) -- points with this object collect history, points without it do not
- Trend Logs folder at box level showed 0 objects -- history lives under individual points
- Retry Trigger: 15-minute interval, runs 24/7
- Total points audited: 879 (414 receiving data, 465 not receiving data)
- Trend audit file: gainesville_trend_audit.xlsx
- **Windows Service Recovery settings (found Aug 6):** All Niagara/Vykon services on the remote desktop have recovery set to "Take No Action" for first, second, and subsequent failures. Should be "Restart the Service" so the BAS station auto-recovers from crashes without manual intervention. Awaiting permission from WWG Gay / Concept Companies to make this change.
- Event Viewer (Application + System) accessible from remote desktop -- useful for diagnosing service crashes and Niagara errors retroactively.
- **History databases (5 separate, per Conner Aug 3):** SAVs and SATs on the 2nd floor vivarium are in `JAX_2nd_Floor`. First floor SAVs 1-5 are in **`FirstFloor_JACE`** -- they reside on a separate network/JACE controller and have always been trending, just under a different history selection. The five available databases are: `FirstFloor_JACE`, `JAX_2nd_Floor`, `LabExhaust_2_Fans`, `LabExhaust_3_Fans_v2`, `OptimizerSupervisor`. To access: in the Niagara history chart viewer, click the green dot in the top-left to open the history database picker, then navigate Histories > FirstFloor_JACE. Enable/disable collection per-point via right-click in the History Ext Manager (Station > History).

---

## Trend Audit -- Non-Reporting Point Summary

| Point Type | Count Not Reporting |
|-----------|-------------------|
| SupplyDmprCmdint | 39 |
| RoomTempint | 38 |
| RHTVLV_POS | 37 |
| RetDamperPos | 35 |
| BoxFlow | 38 |
| expectedRet_CFM | 38 |
| RmPressure_Out | 12 |
| ReheatPosCmd | 7 |
| DischargeTemp | 7 |
| RoomHumidity | 6 |
| RoomTemp | 6 |
| SADamperPOS | 4 |
| ExhaustDamperPos | 3 |
| SAFlowSpt | 3 (never trends by design) |
| Other | various |

Priority boxes to fix first: SAV 3-1, 3-2, 3-4, 3-5, 3-27A, 3-30A (RoomTemp and RoomHumidity)

---

## Room / Space Reference Map (2nd Floor SAV-3 Zones)

Source: Zaal's June 9, 2026 alarm priority assignment email to Wayne Cameron (RE: Gainesville Alarm Priorities -SAV3).

**Priority Tier 1 -- Animal Rooms (tightest control, highest alarm priority):**
- 214 Surgery
- 215 Proc 3
- 216 Proc 4
- 217 Proc 5
- 218 Physio
- 220-225 Behavioural
- 230 Holding 1
- 231 Proc 1
- 232 Holding 2
- 233 Proc 2
- 235 Holding 3

**Priority Tier 2 -- Support Rooms:**
- 240A Lab Supp
- 312 Clean Storage

**Priority Tier 3 -- Labs:**
- 240 Lab 1
- 241 Cell Bio
- 242 Lab 2 (Jun 9 email lists "241 Lab 2" -- likely a typo, should be 242)

**Priority Tier 4 -- Airlock:**
- 301 Airlock

**Priority Tier 5 -- Corridor (lowest priority):**
- 311 Combo

**Known SAV-to-Room Mappings (confirmed from emails):**
- SAV 3-27 = Room 240, Lab 1 (confirmed Jun 24, 2026)
- SAV 3-17 = Procedure Room 4 (confirmed Jul 23, 2026 -- Sonia's escalation). Likely Room 216 based on the room list above, but not explicitly stated in email.

**Alarm Matrix Documents (email attachments, Jun 9 Wayne Cameron email):**
- `Gainesville Alarm Matrix 6_9_26.csv` -- corrected alarm matrix with 10-12 return-to-normal cells that Wayne fixed
- `Alarm Priorities.xlsx` -- BAS alarm priorities reference from JAX BAS standards

**Note on alarm priority updates:** Wayne noticed 10-12 return-to-normal cells had no priority set. He corrected this and resent the matrix June 9. The subsequent alarm priority work in Niagara was implemented around June 15 -- coinciding with the trend logging gap that stopped June 15 and resumed June 17.

---

## August 4-5, 2026 -- Valve Replacement and Post-Restart Humidity Alarms

**August 4 -- Elevator Vestibule Air Valve Replacement:**
- WWG Mechanical shut down RTU-3 for ~1 hour to replace the valve (Sonia OOO; Stockman was backup contact)
- Jonathan Jury (Concept Companies) showed WWG the valve location on-site

**August 5 -- Humidity Alarms After Restart:**
- Sonia notified Jesse and Zaal at 11:27 AM: humidity alarms firing all morning. Initial attribution: "I'm attributing the issue to yesterday's shutdown of RTU-3 (for the replacement of the Elev Vest Air Valve). I asked him if any of the compressors need to be reset." -- Correct that the shutdown triggered the chain, but root cause is compressor failure.
- Jesse's follow-up (1:56 PM): "If the compressors were working as they should be except for #5, but we were still having these humidity issues today, why is my next question?" -- This question was answered by Shelton below and confirmed more fully by Conner on Aug 6.
- Conner (WWG, remote): could see compressors 1, 2, 4 working; compressor 3 working intermittently
- Shelton (WH Construction) arrived on-site Aug 5; found no compressors needed resetting
- Shelton's finding: compressor 5 is actually DOWN (not just on standby). Shelton: "the weather is causing the RTU to show that one of its compressors is actually down. It being down is different from it being on standby. So, the RTU is operating at 80% capacity, not 100%. With one compressor down, the rest of the unit's trying to compensate."
- Answer to Jesse's "why" question: RTU at 80% capacity can't handle full Florida summer heat + dehumidification load. Conner's Aug 6 reply added: circuits 3 and 4 also intermittent -- may be even less than 80% capacity.
- Alarms "considerably subsided" by Sonia's 2:16 PM update
- Stockman (2:45 PM): "WWG Gay said one set of compressors stays off at all times and it rotates to a different bank all the time." Needs confirmation with Conner.
- Sonia (3:01 PM reply to Stockman): "I'll talk to Conner again, but, wouldn't that explain why compressor #3 is working intermittently?" -- Conner's Aug 6 reply confirmed: circuits 3 and 4 have intermittent issues.
- WH Construction (Shelton + team) confirmed arriving Aug 6 at 8-8:30 AM to find/repair compressor 5 refrigerant leak

**New contact found: Shelton (WH Construction)** -- on-site tech who assessed compressors Aug 5. Not the same as Mike Fort or Ashton.

---

## June 23, 2026 -- Supply DP Event (Root of Weekly Review Mandate)

**What happened:**
- Morning of June 23, an air supply loss and recovery occurred at Gainesville
- Jesse Hinkle sent screenshots of Supply DP trend data to Sonia Hopewell and David Stockman (cc: Dave Kuchta)
- Jesse also flagged: LAB 1 SupplyDmprCmdint had no data since February 2025, Holding Room 3 since December 2024 -- both non-reporting trend points

**Dave Kuchta's response (forwarded to Wayne Cameron and Zaal, Red Category):**
- "Please have a look at this event and share your thoughts on what happened."
- "Sooner or later we're going to have a disaster down there."
- **"It is critical that Zaal reviews trends and alarms weekly in detail. That will help reduce the probability of it happening."**

**Zaal's reply:** "10-4 will look at this first thing in the morning and get it sorted out."
**Dave's final reply:** "Great."

This exchange is the direct origin of the weekly BAS trend review requirement.

**Ken Hovey's root cause suggestion ("RTU-3 Static" email):** On June 23 Sonia contacted Ken (WWG Controls). Ken sent a separate email titled "RTU-3 Static" suggesting that the supply DP drop was caused by a **voltage spike or dip** -- recommending review of the Power Meter Data (192.168.15.57) to confirm. Sonia forwarded Ken's email content as embedded screenshots in her June 23 update to Jesse/Kuchta/Zaal. NOTE: This email was never sent directly to Zaal; the content exists only as inline images in Sonia's June 23 email -- not separately searchable. No one is documented to have checked the power meter data in response. The power quality hypothesis remains unverified.

The LAB 1 and Holding Room 3 non-reporting points Jesse flagged became part of the 465 non-reporting points Zaal addressed during the July visit.

---

## WiCom / Allentown Rack Monitoring System

**What it is:** Allentown Wi-Com Cloud -- remote monitoring for blower racks in animal housing rooms. 7 units in GF3. Alarms go to `Gainesville_Allentown_Alarms@jax.org`.

**Key contacts:**
- Karine Lux (JAX, Associate Director) -- oversight / escalation
- Jesse Hinkle (JAX Gainesville) -- on-site coordination
- Ashley Beaton (JAX PQC) -- setpoint review, WiCom user access oversight
- Sabrina Julia (JAX Gainesville) -- on-site initialization of racks
- Gizelle Rosario (JAX Gainesville) -- added to WiCom April 2025
- Stephen Burgess (Allentown) -- WiCom networking support, restart networking ports remotely

**History of issues (April 2025):**
- 6 of 7 units went offline for a week, 1 offline for over a month
- Root cause: networking issue; Stephen Burgess restarted networking ports April 24
- Serial number/Android serial mismatch on some racks -- needed physical identification behind barrier
- After fixing networking: 2 racks came back, but rack info was lost (workaround: re-enter info)
- Sabrina Julia reinitiated 4 blowers on-site

**Remaining blower issues (as of April 2025):**
- Blower 1 in Room 1 -- physically moved to Room 3, still registered in Room 1 profile. Needs to be removed.
- Blower 3 in Room 1 -- display screen issue, can't initialize. Sabrina can try plugging in keyboard to bypass.
- New racks in rooms need to be initialized -- SOP exists (attached to April 24 email)
- Garrett (networking) was scheduled to visit to sort out ports for new racks

**May 2025 update (Jesse):** Most blowers reporting again except one that was moved. Blower that was moved to another room not yet sorted.

**Documents available:**
- `SOP for Adding a New Blower Rack in Gainesville.docx` (attachment in April 24 email)
- `MAN10024_EcoFlo_Manual_v9.pdf` (Allentown blower manual, attachment April 24)
- `Wi-Com Cloud User Manual v1.pdf` (attachment April 24)

Priority boxes to fix first: SAV 3-1, 3-2, 3-4, 3-5, 3-27A, 3-30A (RoomTemp and RoomHumidity)

---

## Early Project History (2025 -- Early 2026)

*Sourced from JAX Closeout List PDF dated March 4, 2026 (David Stockman / Concept Companies, weekly update series)*

### Key Stakeholders Confirmed
- **John Scheckel (JS)** -- JAX senior approver (John.Scheckel@jax.org), approves work orders, budgets, and vendor decisions. Appears as decision-maker throughout 2025-2026 punch list alongside Kuchta.
- **AEI** -- Design/commissioning engineering firm for the project. Kelly (last name unknown) was commissioning engineer who signed off on systems.
- **Fitz / John Fitz** -- AEI contact who authorized Schneider power meter programming and MSA agreements.
- **Newton Freire** -- JAX Project Manager for Lab 2 modifications (Chemical Room build-out, door between Cell Bio and Lab Supply).
- **Hank Pate (HP)** -- Concept Companies Facilities Manager, frequent on-site coordinator. On March 4 closeout he was asked to get Ken to add Jesse and Zaal to BAS login.

### BAS Access Timeline
- **March 4, 2026**: Hank Pate was explicitly asked to "ask Ken to add Jessie and Zaal for log in BAS" (Item C). This is when Zaal's BAS access was initiated.

### RTU-3 Early Instability
- **July 21, 2025**: RTU-3 lost status at 10:38. SAV-AHU status lost, Supply DP alarms at 10:40. Ken noted he was "not sure what happened during this shut down." First documented RTU-3 instability event.
- **Item V (March 2026 closeout list)**: "Ken/Kyle valve may be stuck...WWGay needs to be more vetted...may be a power issue voltage." First documented reference to stuck valve concern. Predates the summer 2026 crisis by months.

### RTU-3 Freeze Stat -- Full Timeline (CONFIRMED)
- **Feb 2, 2026**: WWG Gay ordered freeze stat replacement.
- **Feb 18, 2026**: Hank Pate expected part in "about a week."
- **March 4, 2026**: Part on-site. Scheduling delayed -- Jesse to provide time.
- **March 18, 2026**: Checking on overtime / JAX lab staff availability.
- **March 25, 2026**: HP spoke to vendor, looking 2 weeks out.
- **April 9, 2026**: Work originally set for this date -- rescheduled.
- **April 22, 2026**: New date needed. Jesse provided dates for 2:30 start.
- **April 29, 2026**: May 13 identified as preferred date.
- **May 1, 2026**: Wade Godwin (NCJax) confirmed for May 13 at 2 PM.
- **May 13, 2026**: **FREEZE STAT INSTALLED.** Done by Wade Godwin (NCJax) at 2 PM. Source: JAX Weekly List 6.17.26.pdf.
- **May 20, 2026**: Sonia raises seasonal stability question -- only 7 days after installation.

### BAS Access Timeline (CONFIRMED)
- **March 4, 2026**: HP (Hank Pate) asked to "ask Ken to add Jesse and Zaal for log in BAS."
- **April 1, 2026**: No response yet from Ken.
- **May 6, 2026**: BAS access given to both Jesse and Zaal.
- **May 27, 2026**: BAS access reissued -- initial access had expired. Both logged in successfully.
- **June 14, 2026**: Jesse lost access again -- JAX IT issue. Brandon Shakespeare resolving.

### Additional Milestones (from JAX Weekly List 6.17.26.pdf)
- **May 13, 2026**: Freeze stat replaced (see above).
- **May 26, 2026**: RTU-4 serviced (NCJax or contractor, listed as complete in June 17 closeout).
- **June 3, 2026**: Elevator vestibule valve identified as bad (Room 314/317/311 alarm). "Looks like a bad air valve needs to be replaced." -- resolved Aug 4, 2026.
- **June 3, 2026**: Ken (WWG) admitted he did not understand flush cycle behavior: "I will need to do some research on my end to understand and address the flush cycle issue that is being described. We will reach out and let you know what we find out. Please feel free to ask any questions, I just don't have answers at this point in regards to the humidifiers flush cycle." This is the earliest documented confirmation that WWG does not have flush cycle visibility.
- **June 14, 2026**: B&D Electric installed ambient light sensor in Procedure Room 5 and cognition room dimmer control box (separate from RTU work).
- **June 17, 2026**: Latest closeout list issued (JAX Weekly List 6.17.26.pdf).

### New Contacts from June 17 Closeout List
- **Will Leduc** (Concept Companies, on-site facilities): checks ceilings for leaks, coordinates with Jesse, installs fixtures (shelving, door sweeps, etc.)
- **Christian** (WWG Gay, after-hours tech): handled CO2 leak response July 24, 2025. Not the same as Conner.
- **Brian Crawford** (Concept Companies, brian@conceptcompanies.net): reviews MSA agreements and contracts.
- **Kelly** (AEI, commissioning engineer): signed off on commissioning; issued generator test report; coordinates boiler testing. Full last name not documented.

### Infrastructure Milestones (2025-2026)
- **July 2025**: Boiler switching instability. Ken programmed temperature threshold to fix automatic switchover. Resolved August 2025.
- **July 10, 2025**: UPS incident -- Conner tested backfeed; wrong breaker cut power to 2nd floor Mechanical Room control panel (Boilers, LEF, Cage Rack, AHUs 1-4). Multiple panel labels were incorrect.
- **August 2025**: Pressure stability QC completed. RTU compressor rotation mode confirmed.
- **January 11, 2026**: New server installed by Epic IT Solutions. Credentials sent to Kyle Martin and Dave Kuchta. Cove Data Protection backup + NinjaOne remote access configured.
- **January 14, 2026**: New Schneider PM5650 power meter installed (Bacnet alarming for electric stability). Bob Terwilliger handled server/port setup. Kyle Martin coordinates with Epic IT.

### Humidity Tuning History (Nov 2025 -- Feb 2026)
- **Nov 12, 2025**: "Review cold events and settings to control. DK: write program to activate second system for duplication to handle swings." Origin of the parallel humidifier operation project.
- **Dec 3, 2025**: "JS [John Scheckel]: get AEI back on board to tune the humidifier. WWGay to reprogram."
- **Dec 10, 2025**: Ken adjusted humidifier settings. "Need a little time to see if it's working correctly."
- **Jan 14, 2026**: New supply duct humidity sensor on order, to be relocated. (Ken installed ~Feb 27, 2026.)
- **Feb 11, 2026**: Kuchta asked "all tuned? Update status of programming." No clear confirmation in record.

### SAV-Related Early Work
- **SAV 3-6 pressure binary change**: Documented as complete in March 4 closeout list. Part of early commissioning pressure sensor work.
- **VHP barrier coordination (Aug 2025)**: SAVs near VHP require coordination with Jesse for backfeed checks. Ken confirmed backfeed not needed, August 15, 2025.

---

## Self-Assessment -- How to Improve as the Gainesville BAS Tech

*Compiled from full email sweep, June-August 2026. These are systemic patterns, not one-time mistakes.*

### 1. Weekly Review Was Mandated -- But the Crisis Still Hit
Dave Kuchta established the weekly BAS trend review requirement on June 23, after the supply DP event. The compressor failure built throughout July -- Conner's Jul 28 analysis showed RTU-3 had 3 of 5 compressors off, causing supply air to run at 67°F. This condition should have been visible in weekly trend reviews as an anomalously low supply air temperature combined with rising humidity. The crisis hitting on August 5 suggests the weekly review either wasn't happening or wasn't catching supply air temperature trends in addition to humidity alarms.

**Improvement:** When doing weekly BAS reviews, check RTU supply air temperature, not just room humidity. A supply temp above setpoint = RTU dehumidification capacity problem, not just a setpoint issue.

### 2. You Were Not in the Alarm Path for Proc Rm 4
On July 20-21, the front desk BAS screen stopped receiving Proc Rm 4 humidity alarms at 10:11 AM (humidity: 71%). By the next morning, humidity was at 89% -- Jesse caught it with a handheld reader, not BAS. The alarm was not delivered to you either. Mark Garcia asked Sonia if a tech should check the screen -- it is not documented that a tech was ever dispatched or that the root cause of the alarm delivery failure was found.

**Improvement:** BAS alarms for animal rooms should be delivered directly to your email/phone (Niagara alarm routing), not only to a front desk screen. The front desk screen is an auxiliary display, not a reliable alert mechanism.

### 3. Conner's Jul 16 Dehumidification Proposal Was Not Escalated
On July 16 -- four days before your visit -- Conner told Sonia: "If JAX is open to another program addition that would allow the animal rooms to go below 69°F towards 66-65°F to allow dehumidification." This was sent to Sonia and Mark Garcia, not to Zaal or Kuchta. No JAX response is documented. By the time of the Jul 20-22 visit, this option had not been discussed or implemented.

**Improvement:** Conner's technical recommendations that require JAX approval (setpoint changes, program additions) need to reach Kuchta or Cameron, not just Sonia. When WWG sends a solution to Sonia only, it gets stranded. Your job is to pull technical proposals out of the Sonia relay and route them up the JAX chain.

### 4. Vendor Follow-Through Requires Active Pushing
Several commitments were made and not kept without a follow-up nudge:
- Ken promised to research flush cycles (Jun 3) -- never did. Meeting never happened.
- Alarm priorities were flagged June 8 after the GF3 Priority 255 incident -- never fixed before the crisis.
- Mark Garcia asked Sonia if a tech should check the front desk alarm screen (Jul 21) -- no confirmation a tech ever came.
- WWG's general pattern: they ask "would you like us to schedule a tech?" rather than acting. They respond well when given a specific request but do not self-initiate.

**Improvement:** When a vendor makes a commitment, put it in the punch list and set a follow-up date. If no confirmation in 5-7 business days, send one explicit follow-up email naming the outstanding item. Don't let open items sit in Sonia's inbox.

### 5. RTU Architecture Was Unknown Until the Visit
Before July 20, the two-layer RTU control structure (Honeywell BAS layer + AnnexAir local compressor control layer) was not documented anywhere. The fact that BAS can show "compressors commanded on" while AnnexAir shows them physically faulted was discovered during the crisis. Similarly, the Rht_Modulation = preheat 3-way valve controlling hot water from boiler was only clarified Aug 6 by Conner.

**Improvement:** After each technical discovery, add it to the BAS System Notes section immediately. Gaps in system documentation mean that next time you see a weird BAS reading, you won't know what it represents. The goal is to never need Conner to explain how the RTU works a second time.

### 6. BAS Access for Jesse Was Delayed 60+ Days
Jesse requested BAS access March 4, 2026. It was not provided until May 6, 2026 -- more than two months later. Without BAS access, Jesse had no ability to verify alarm conditions himself and had to rely on the front desk screen or calling Sonia. The Jun 8 GF3 Priority 255 incident was detected by Jesse's team visiting the room, not by BAS.

**Improvement:** Jesse having BAS access is a force multiplier -- he's on-site every day. Prioritize keeping his access current and make sure he knows the key views (room humidity, supply air temp, alarm screen). When his access lapsed again in June, it took two weeks to restore. Treat BAS access for on-site ops like a utility, not a one-time task.

### 7. Communication Was Informal at First, Then Became Structured
Your July 20 arrival email ("I am onsite as the bar harbor Jackson labs building automation tech in charge of monitoring our gainsville controls. I need support and assistance with some issues on campus") was sent from your phone and lacked specifics about what you needed. Compare that to your July 22 post-visit recap with 10 prioritized action items -- that format is much more effective.

**Improvement:** Before on-site visits, send a brief agenda email (3-5 bullet items) listing what you intend to address. It sets expectations, pulls the right people into the conversation, and creates a paper trail. Your Jul 27 three-item follow-up email to Conner is a good template -- lead with a numbered list, keep it short.

### 8. The JACE Quote ($737.28) Sat Open for 9 Days Before Escalation
The quote was received July 22 (attached to your site visit recap). You followed up July 27. It took until August 5 for Stockman to confirm approval -- 14 days total. For a sub-$1,000 item that prevents JACE offline alerts, that is a slow cycle.

**Improvement:** For small-dollar items (under $2,000) that directly affect alarm delivery, flag them explicitly to Kuchta with a recommended approval response: "I recommend approving -- this prevents us from missing JACE offline events." Give decision-makers a yes/no question, not an open-ended review request.

### 9. Power Meter Data Was Never Checked
Ken suggested checking 192.168.15.57 for a voltage spike or dip after the Jun 23 supply DP event. Nobody checked. It remains unverified whether power quality contributed to the Jun 23 event and whether it has happened since.

**Improvement:** This is a 10-minute task. Log into the power meter via Firefox (credentials from Bob Terwilliger), pull the Jun 23 event window, and document what you find. It either explains the DP event (useful) or rules out power quality (also useful). Items like this should not stay on the punch list for months.

### Summary Pattern
The recurring theme is **open items that were acknowledged but not closed.** Alarm priorities flagged and not fixed. Flush cycle meeting promised and not scheduled. Vendor commitments made and not confirmed. RTU architectural knowledge not documented. The visit itself was excellent -- the Jul 22 recap email and subsequent follow-ups show strong technical judgment. The gap is the weeks before and after, when items drift without a forcing function.

The weekly BAS review is the primary habit to build: 30 minutes, every Monday, check supply air temps, preheat valve positions, compressor statuses, and trending points. Most of this summer's crisis was visible in that data before it became a crisis.
