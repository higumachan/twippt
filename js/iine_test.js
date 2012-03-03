(function() {
	  var host, iine, send_iine, socket, status;

	    status = $("#status");

		  iine = $("#iine");

		    host = location.href.match(/localhost/) ? "http://" + location.host + "/" : 'http://xhago.nodester.com/';

			  socket = io.connect(host);

			    send_iine = function() {
					    return socket.send("iine");
						  };

						    socket.on("connect", function() {
								    status.text("connected");
									    return iine.bind("click", send_iine);
										  }).on("disconnect", function() {
											      status.text("disconnected");
												      return iine.unbind("click", send_iine);
													    }).on("message", function(count) {
															    var css_props, e, iyo, text;
																    iine.text("(・∀・)イイネ!×" + (+count));
																	    if (+count % 150 === 0 && +count !== 0) {
																			      iyo = $("<embed hidden='true'>").attr({
																					          src: "/sound/iyopon.mp3",
																							          autostart: true
																									        });
																				        $("body").append(iyo);
																						      return setTimeout(function() {
																								          $("#sugoku").removeClass("hidden");
																										          return $("#sugoku").fadeIn("fast", function() {
																													            return setTimeout(function() {
																																	            return $("#sugoku").addClass("hidden");
																																				          }, 12000);
																																        });
																												        }, 3100);
																							      } else {
																									        text = "(・∀・)イイネ!";
																											      css_props = {
																													          "font-size": 40 * Math.random() + 10,
																															          "white-space": "nowrap",
																																	          top: ($(window).height() - 20) * Math.random(),
																																			          left: ($(window).width() - 100) * Math.random(),
																																					          position: "fixed"
																																							        };
																																									      e = $("<div></div>").text(text).css(css_props);
																																										        e.fadeIn("fast", function() {
																																													        return $(this).fadeOut("slow", function() {
																																																          return $(this).remove();
																																																		          });
																																															      });
																																												      return $(document.body).append(e);
																																													      }
																																														    });

}).call(this);

