entity_id = data.get('entity_id')
end_brightness = int(data.get('brightness'))
transition = int(data.get('transition'))

SMOOTH = 2
STEPS = transition * SMOOTH
SLEEP_TIME = 1 / SMOOTH

states = hass.states.get(entity_id)

if states is not None:
	state_brightness = states.attributes.get('brightness') if states.state == 'on' else 0
	step = (end_brightness - state_brightness) / STEPS
	current_level = state_brightness
	for x in range(1, STEPS + 1):
		next_level = int(state_brightness + step * x)
		if current_level != next_level:
			data = {"entity_id": entity_id, "brightness": next_level}
			hass.services.call('light', 'turn_on', data)
		current_level = next_level
		time.sleep(SLEEP_TIME)
else:
	logger.error(f'Wrong {entity_id}')