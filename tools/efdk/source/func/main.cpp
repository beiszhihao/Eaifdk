#include <iostream>
#include <cstdlib>
#include <gflags/gflags.h>
using namespace std;

DEFINE_bool(train, false, "Start training");
DEFINE_bool(build, false, "Compile model");
DEFINE_bool(test, false, "Test result");
DEFINE_bool(see, false, "View training model");
DEFINE_bool(board, false, "View training panel");
DEFINE_bool(anchors, false, "Calculate recommended anchor points for training set");
DEFINE_bool(reName, false, "Unified image file name, arg:--path --prefix");
DEFINE_bool(map, false, "View average KPI indicators");
DEFINE_bool(recall, false, "Calculate recall rate");
DEFINE_string(update, "", "Update dataset");
DEFINE_string(view, "", "View model struct");
DEFINE_string(autoLabel, "", "Auto label image");
DEFINE_string(path, "", "Specify path");
DEFINE_string(prefix, "", "File prefix");
DEFINE_string(samples, "", "Build sample project");

template <typename T>
int event(int flags, T arg) {
	string arg_cmd = "";

	switch (flags) {
		case 1:
			system("bash $EAIFDK_HOME/script/train.sh");
			break;
		case 2:
			system("bash $EAIFDK_HOME/script/build.sh");
			break;
		case 3:
			system("bash $EAIFDK_HOME/script/test.sh");
			break;
		case 4:
			system("bash $EAIFDK_HOME/script/seeWeights.sh");
			break;
		case 5:
			system("bash $EAIFDK_HOME/script/board.sh");
			break;
		case 6:
			system("bash $EAIFDK_HOME/script/anchors.sh");
			break;
		case 7:
			system("bash $EAIFDK_HOME/script/mAP.sh");
			break;
		case 8:
			system("bash $EAIFDK_HOME/script/recall.sh");
			break;
		case 9:
			arg_cmd = "bash $EAIFDK_HOME/script/update.sh " + arg;
			system(arg_cmd.c_str());
			break;
		case 10:
			arg_cmd = "bash $EAIFDK_HOME/script/view.sh " + arg;
			system(arg_cmd.c_str());
			break;
		case 11:
			arg_cmd = "bash $EAIFDK_HOME/script/autoLabel.sh " + arg;
			system(arg_cmd.c_str());
			break;
		case 12:
			arg_cmd = "bash $EAIFDK_HOME/script/reName.sh " + FLAGS_path + " " + FLAGS_prefix;
			system(arg_cmd.c_str());
			break;
		case 13:
			arg_cmd = "bash $EAIFDK_HOME/script/sample.sh " + FLAGS_samples;
			system(arg_cmd.c_str());
			break;

	}

	return 0;
}

int main(int argc, char* argv[]) {
	gflags::SetVersionString ("1.0.0.0");
	gflags :: SetUsageMessage ("Usage: efdk [options] ...");	
	gflags::ParseCommandLineFlags(&argc, &argv, true);	
	if(FLAGS_train) {
		event(1, 0);
	}
	if(FLAGS_build) {
		event(2, 0);
	}
	if(FLAGS_test) {
		event(3, 0);
	}
	if(FLAGS_see) {
		event(4, 0);
	}
	if(FLAGS_board) {
		event(5, 0);
	}
	if(FLAGS_anchors) {
		event(6, 0);
	}
	if(FLAGS_map) {
		event(7, 0);
	}
	if(FLAGS_recall) {
		event(8, 0);
	}
	if(FLAGS_update != "") {
		event(9, FLAGS_update);
	}
	if(FLAGS_view != "") {
		event(10, FLAGS_view);
	}
	if(FLAGS_autoLabel != "") {
		event(11, FLAGS_autoLabel);
	}
	if(FLAGS_reName) {
		event(12, 0);
	}
	if(FLAGS_samples != "") {
		event(13, FLAGS_samples);
	}

	return 0;
}
