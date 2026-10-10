const CheckIn = require("../models/CheckIn");
const { computeStressWithAI } = require("../services/aiService");
const { checkAndTriggerStressAlert } = require("../services/alertService");

const createOrUpdateCheckIn = async (req, res) => {
  const {
    sleep,
    study,
    screen,
    exam,
    mood,
    note,
    nervousness,
    unable_to_control,
    unableToControl,
    worry,
    trouble_in_relaxation,
    troubleInRelaxation,
    restlessness,
    irritability,
    fear,
  } = req.body;

  // Normalize aliases
  const normUnableToControl = unable_to_control !== undefined ? unable_to_control : unableToControl;
  const normTroubleInRelaxation = trouble_in_relaxation !== undefined ? trouble_in_relaxation : troubleInRelaxation;

  // Validate academic and lifestyle inputs
  if (sleep === undefined || isNaN(Number(sleep)) || Number(sleep) < 0 || Number(sleep) > 24) {
    return res.status(400).json({ message: "Invalid sleep hours. Must be a number between 0 and 24." });
  }
  if (study === undefined || isNaN(Number(study)) || Number(study) < 0 || Number(study) > 24) {
    return res.status(400).json({ message: "Invalid study hours. Must be a number between 0 and 24." });
  }
  if (screen === undefined || isNaN(Number(screen)) || Number(screen) < 0 || Number(screen) > 24) {
    return res.status(400).json({ message: "Invalid screen hours. Must be a number between 0 and 24." });
  }
  if (exam === undefined || isNaN(Number(exam)) || Number(exam) < 0) {
    return res.status(400).json({ message: "Invalid exam proximity. Must be a non-negative number of days." });
  }

  // Validate required GAD-7 clinical questionnaire features
  const clinicalFields = {
    nervousness,
    unable_to_control: normUnableToControl,
    worry,
    trouble_in_relaxation: normTroubleInRelaxation,
    restlessness,
    irritability,
    fear,
  };

  for (const [key, val] of Object.entries(clinicalFields)) {
    if (val === undefined || val === null || isNaN(Number(val)) || Number(val) < 0 || Number(val) > 3) {
      return res.status(400).json({
        message: `Invalid or missing clinical assessment field '${key}'. Must be an integer between 0 and 3 (0: No, 1: Mild, 2: Moderate, 3: Severe).`,
      });
    }
  }

  const todayDate = new Date().toISOString().split("T")[0];

  // Call FastAPI ML service with both clinical features and daily context
  const aiResult = await computeStressWithAI({
    sleep: Number(sleep),
    study: Number(study),
    screen: Number(screen),
    exam: Number(exam),
    mood: mood || "okay",
    note: note || "",
    nervousness: Number(nervousness),
    unable_to_control: Number(normUnableToControl),
    worry: Number(worry),
    trouble_in_relaxation: Number(normTroubleInRelaxation),
    restlessness: Number(restlessness),
    irritability: Number(irritability),
    fear: Number(fear),
  });

  if (!aiResult) {
    return res.status(503).json({
      message: "Machine Learning stress inference service is temporarily unavailable. Please try again shortly.",
    });
  }

  const checkInData = {
    userId: req.user._id,
    date: todayDate,
    sleep: Number(sleep),
    study: Number(study),
    screen: Number(screen),
    exam: Number(exam),
    mood: mood || "okay",
    note: note || "",
    nervousness: Number(nervousness),
    unableToControl: Number(normUnableToControl),
    worry: Number(worry),
    troubleInRelaxation: Number(normTroubleInRelaxation),
    restlessness: Number(restlessness),
    irritability: Number(irritability),
    fear: Number(fear),
    stressScore: aiResult.score,
    stressLevel: aiResult.level,
    mlPrediction: aiResult.mlPrediction || null,
    recommendations: aiResult.recommendations,
  };

  const checkIn = await CheckIn.findOneAndUpdate(
    { userId: req.user._id, date: todayDate },
    checkInData,
    { new: true, upsert: true }
  );

  // High stress streak evaluation
  await checkAndTriggerStressAlert(req.user, aiResult.level);

  res.status(200).json(checkIn);
};

const getTodayCheckIn = async (req, res) => {
  const todayDate = new Date().toISOString().split("T")[0];
  const checkIn = await CheckIn.findOne({ userId: req.user._id, date: todayDate });
  res.json(checkIn || null);
};

const getWeeklyHistory = async (req, res) => {
  const checkIns = await CheckIn.find({ userId: req.user._id })
    .sort({ date: -1 })
    .limit(7);

  res.json(checkIns.reverse());
};

module.exports = { createOrUpdateCheckIn, getTodayCheckIn, getWeeklyHistory };