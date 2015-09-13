Parse.Cloud.beforeSave("citations", function(request, response) {
  if (!request.object.get("proactive_outreach")) {
    request.object.set("proactive_outreach", false);
  }
  if (!request.object.get("court_address")) {
  	court_address = ''
    request.object.set("court_address", false);
  }

  response.success();
});

Parse.Cloud.beforeSave("violations", function(request, response) {
  if (!request.object.get("proactive_outreach")) {
    request.object.set("proactive_outreach", false);
  }

  response.success();
});