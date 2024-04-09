#include "backend/player_command.hpp"
#include "core/scr_globals.hpp"
#include "natives.hpp"
#include "pointers.hpp"

#include <script/globals/GPBD_FM_3.hpp>

namespace big
{
	class send_fake_ban_message : player_command
	{
		using player_command::player_command;

		virtual CommandAccessLevel get_access_level() override
		{
			return CommandAccessLevel::AGGRESSIVE;
		}

		virtual void execute(player_ptr player, const command_arguments& _args, const std::shared_ptr<command_context> ctx) override
		{
			const size_t arg_count  = 9;
			int64_t args[arg_count] = {(int64_t)eRemoteEvent::SendTextLabelSMS, (int64_t)self::id, 1i64 << player->id()};

			::strcpy_s((char*)&args[2], (arg_count - 2) * sizeof(*args), "HUD_ROSBANPERM");

			g_pointers->m_gta.m_trigger_script_event(1, args, arg_count, 1 << player->id(), (int)eRemoteEvent::SendTextLabelSMS);
		}
	};

	send_fake_ban_message g_send_fake_ban_message("fakeban", "FAKE_BAN_MESSAGE", "FAKE_BAN_MESSAGE_DESC", 0);
}