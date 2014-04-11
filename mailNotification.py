import weechat, string
import simplemail
import hashlib

weechat.register("mailNotify", "Ik4ru5", "0.1", "UNKOWN", "mailNotify - A Mail notification plugin for weechat", "", "")

# Set up here, go no further!
settings = {
	"show_highlight"	: "on",
	"show_priv_msg"		: "on",
	"show_icon"			: "weechat",
	"from_name"			: "Weechat Messages",
	"from_mail"			: "",
	"to"				: "",
	"challenge_key"		: ""
}
####################
# TODO Blacklist! 
####################

for option, default_value in settings.items():
	if weechat.config_get_plugin(option) == "":
		weechat.config_set_plugin(option, default_value)

# Hook privmsg/hilights
weechat.hook_print("", "irc_privmsg", "", 1, "get_notified", "")

# Functions
def get_notified(data, bufferp, uber_empty, tagsn, isdisplayed, ishilight, prefix, message):
	#######################
	# TODO Spam protection
	#######################
	
	
	# Private Message	
	if (weechat.buffer_get_string(bufferp, "localvar_type") == "private" and weechat.config_get_plugin('show_priv_msg') == "on"):
		buffer = (weechat.buffer_get_string(bufferp, "short_name") or weechat.buffer_get_string(bufferp, "name"))
		if buffer == prefix:
			weechat.prnt('', '[DEBUG][%s]Private Message from %s: %s' % (buffer, prefix, message))
			authToken = hashlib.md5()
			authToken.update("s%s%" % (prefix, weechat.config_get_plugin('challenge_key')))
			simplemail.Email(
				from_address = u"%s <%s>" % (weechat.config_get_plugin('from_name'), weechat.config_get_plugin('from_mail')),
				to_address = u"%s" % (weechat.config_get_plugin('to')),
				subject = u"Message from: %s [%s]" % (prefix, authToken.hexdigest()),
				message = u"Message from %s: %s" % (prefix, message)).send()

	# Highlighting
	elif (ishilight == "1" and weechat.config_get_plugin('show_highlight') == "on"):
		buffer = (weechat.buffer_get_string(bufferp, "short_name") or weechat.buffer_get_string(bufferp, "name"))
		weechat.prnt('', '[DEBUG][%s]Highlight from %s: %s' % (buffer, prefix, message))
		simplemail.Email(
				from_address = u"%s <%s>" % (weechat.config_get_plugin('from_name'), weechat.config_get_plugin('from_mail')),
				to_address = u"%s" % (weechat.config_get_plugin('to')),
				subject = u"Highlight from: %s" % (prefix),
				message = u'''In Buffer: %s 
	from %s
%s''' % (buffer, prefix, message)).send()
			

	return weechat.WEECHAT_RC_OK
